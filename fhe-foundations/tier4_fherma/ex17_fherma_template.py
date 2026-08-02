"""Exercise 17 -- Dissecting a FHERMA Challenge Structure

FHERMA (fherma.io) challenges follow a consistent pattern:

  1. A **config** specifies the scheme, security level, depth budget,
     and accuracy threshold.
  2. The participant implements a **solution function** that takes
     (encrypted) inputs and returns (encrypted) outputs.
  3. The platform **validates** the submission: does the output meet
     accuracy requirements?  Does it respect the depth budget?

This exercise builds a *mock* challenge framework in pure Python (no
FHE libraries needed).  The structure mirrors real FHERMA submissions
so you can practice the workflow before touching actual ciphertexts.

We use the "approximate sigmoid on [-8, 8]" challenge as a running
example -- this is a common FHERMA challenge type and connects
directly to the Chebyshev work in ex14.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from check import check, summary

import math


# ---------------------------------------------------------------------------
# Chebyshev utilities (self-contained, mirrors ex14)
# ---------------------------------------------------------------------------

def _chebyshev_nodes(n, a, b):
    """n Chebyshev nodes on [a, b]."""
    nodes = []
    for k in range(n):
        theta = (2 * k + 1) * math.pi / (2 * n)
        nodes.append((a + b) / 2.0 + (b - a) / 2.0 * math.cos(theta))
    return nodes


def _chebyshev_coefficients(f, n, a, b):
    """Compute n Chebyshev coefficients of f on [a, b]."""
    nodes = _chebyshev_nodes(n, a, b)
    f_vals = [f(x) for x in nodes]
    coeffs = []
    for j in range(n):
        s = sum(f_vals[k] * math.cos(j * (2 * k + 1) * math.pi / (2 * n))
                for k in range(n))
        coeffs.append((2.0 / n) * s)
    coeffs[0] /= 2.0
    return coeffs


def _eval_chebyshev(coeffs, x, a, b):
    """Evaluate Chebyshev expansion at x via Clenshaw recurrence."""
    t = (2.0 * x - (a + b)) / (b - a)
    n = len(coeffs)
    if n == 0:
        return 0.0
    if n == 1:
        return coeffs[0]
    b_next2 = 0.0
    b_next1 = 0.0
    for k in range(n - 1, 0, -1):
        b_k = coeffs[k] + 2.0 * t * b_next1 - b_next2
        b_next2 = b_next1
        b_next1 = b_k
    return coeffs[0] + t * b_next1 - b_next2


def make_chebyshev_approx(f, degree, a, b):
    """Return a callable that approximates f on [a, b] with a Chebyshev polynomial."""
    coeffs = _chebyshev_coefficients(f, degree, a, b)
    return lambda x: _eval_chebyshev(coeffs, x, a, b)


# ---------------------------------------------------------------------------
# Exercise functions
# ---------------------------------------------------------------------------

def parse_challenge_config(config_dict):
    """Extract key parameters from a FHERMA-style challenge config.

    Parameters
    ----------
    config_dict : dict
        Must contain keys: 'scheme', 'security_level', 'max_depth',
        'accuracy_threshold', 'domain', 'target_function'.

    Returns
    -------
    dict
        Parsed config with the same keys, validated for required fields.

    Raises
    ------
    ValueError
        If a required key is missing.
    """
    required_keys = [
        "scheme", "security_level", "max_depth",
        "accuracy_threshold", "domain", "target_function",
    ]
    for key in required_keys:
        if key not in config_dict:
            raise ValueError(f"Missing required config key: {key}")

    return {
        "scheme": config_dict["scheme"],
        "security_level": config_dict["security_level"],
        "max_depth": config_dict["max_depth"],
        "accuracy_threshold": config_dict["accuracy_threshold"],
        "domain": tuple(config_dict["domain"]),
        "target_function": config_dict["target_function"],
    }


def validate_submission(solution_fn, test_inputs, expected_outputs, config):
    """Validate a FHERMA-style submission against test cases.

    Parameters
    ----------
    solution_fn : callable
        The candidate solution: takes a float, returns a float.
    test_inputs : list[float]
        Input test points.
    expected_outputs : list[float]
        Expected (true) outputs at test_inputs.
    config : dict
        Parsed challenge config (from parse_challenge_config).

    Returns
    -------
    dict
        {
            'passed': bool,
            'max_error': float,
            'accuracy_threshold': float,
            'accuracy_ok': bool,
            'n_tests': int,
            'errors': list[float],
        }
    """
    errors = []
    for x_in, y_expected in zip(test_inputs, expected_outputs):
        y_got = solution_fn(x_in)
        errors.append(abs(y_got - y_expected))

    max_err = max(errors)
    threshold = config["accuracy_threshold"]
    accuracy_ok = max_err <= threshold

    return {
        "passed": accuracy_ok,
        "max_error": max_err,
        "accuracy_threshold": threshold,
        "accuracy_ok": accuracy_ok,
        "n_tests": len(test_inputs),
        "errors": errors,
    }


def mock_challenge():
    """Return a sample FHERMA challenge: approximate sigmoid on [-8, 8].

    Returns
    -------
    config : dict
        Challenge configuration.
    test_inputs : list[float]
        Test input points.
    expected_outputs : list[float]
        Expected sigmoid values at test_inputs.
    """
    sigmoid = lambda x: 1.0 / (1.0 + math.exp(-x))

    config = {
        "scheme": "CKKS",
        "security_level": 128,
        "max_depth": 15,
        "accuracy_threshold": 0.1,
        "domain": [-8.0, 8.0],
        "target_function": "sigmoid",
    }

    # Generate test points: uniform grid on the domain
    n_test = 200
    a, b = config["domain"]
    test_inputs = [a + (b - a) * i / (n_test - 1) for i in range(n_test)]
    expected_outputs = [sigmoid(x) for x in test_inputs]

    return config, test_inputs, expected_outputs


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
print("=== ex17: FHERMA Challenge Template ===\n")

# --- Test 1: parse_challenge_config ---
raw_config, test_inputs, expected_outputs = mock_challenge()
config = parse_challenge_config(raw_config)
check("config scheme is CKKS", config["scheme"], "CKKS")
check("config security_level is 128", config["security_level"], 128)
check("config max_depth is 15", config["max_depth"], 15)
check("config accuracy_threshold is 0.1", config["accuracy_threshold"], 0.1)
check("config domain is (-8, 8)", config["domain"], (-8.0, 8.0))

# --- Test 2: missing key raises ValueError ---
try:
    parse_challenge_config({"scheme": "CKKS"})  # missing other keys
    check("missing key raises ValueError", False)
except ValueError:
    check("missing key raises ValueError", True)

# --- Test 3: degree-11 Chebyshev should PASS the challenge ---
sigmoid = lambda x: 1.0 / (1.0 + math.exp(-x))
approx_11 = make_chebyshev_approx(sigmoid, 11, -8, 8)
result_11 = validate_submission(approx_11, test_inputs, expected_outputs, config)
print(f"  Degree-11 Chebyshev: max_error = {result_11['max_error']:.6f}, "
      f"threshold = {result_11['accuracy_threshold']}")
check("degree-11 passes challenge", result_11["passed"], True)

# --- Test 4: degree-3 Chebyshev should FAIL the challenge ---
approx_3 = make_chebyshev_approx(sigmoid, 3, -8, 8)
result_3 = validate_submission(approx_3, test_inputs, expected_outputs, config)
print(f"  Degree-3 Chebyshev:  max_error = {result_3['max_error']:.6f}, "
      f"threshold = {result_3['accuracy_threshold']}")
check("degree-3 fails challenge", result_3["passed"], False)

# --- Test 5: validation result structure ---
check("result has 'passed' key", "passed" in result_11)
check("result has 'max_error' key", "max_error" in result_11)
check("result has correct n_tests", result_11["n_tests"], len(test_inputs))

# --- Summary of mock challenge ---
print(f"\n  Mock Challenge: 'Approximate sigmoid on [-8, 8]'")
print(f"    Scheme:             {config['scheme']}")
print(f"    Security level:     {config['security_level']}-bit")
print(f"    Max depth:          {config['max_depth']}")
print(f"    Accuracy threshold: {config['accuracy_threshold']}")
print(f"    Test points:        {result_11['n_tests']}")
print(f"    Degree-3 result:    {'PASS' if result_3['passed'] else 'FAIL'} "
      f"(error={result_3['max_error']:.4f})")
print(f"    Degree-11 result:   {'PASS' if result_11['passed'] else 'FAIL'} "
      f"(error={result_11['max_error']:.6f})")

summary()
