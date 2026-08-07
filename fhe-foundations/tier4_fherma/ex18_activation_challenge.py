"""Exercise 18 -- Optimize Polynomial Activations Under Depth Budget (Capstone)

This is the capstone exercise for the FHE foundations course.  It simulates
a FHERMA-style optimization problem:

    Given a target activation function, a domain, and a maximum allowed
    error, find the *lowest-degree* Chebyshev polynomial approximation
    that meets the error constraint.

Why lowest degree?  In FHE, the degree of the polynomial directly controls
the multiplicative depth of the circuit.  Lower degree = fewer levels =
faster evaluation = lower noise accumulation.  So the optimization target
is: **minimize depth while meeting accuracy.**

This mirrors the exact workflow for FHERMA activation function challenges:
  1. Pick a target function (sigmoid, ReLU, GELU, ...).
  2. Try Chebyshev approximations at increasing degree.
  3. Stop at the first degree that meets the error threshold.
  4. Report the (degree, max_error, passes) triple.

All functions are self-contained (Chebyshev utilities are inlined).
No FHE library is required.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from check import check, summary

import math


# ---------------------------------------------------------------------------
# Chebyshev utilities (self-contained)
# ---------------------------------------------------------------------------

def _chebyshev_nodes(n, a, b):
    """n Chebyshev nodes of the first kind on [a, b]."""
    return [(a + b) / 2.0 + (b - a) / 2.0 * math.cos((2 * k + 1) * math.pi / (2 * n))
            for k in range(n)]


def _chebyshev_coefficients(f, n, a, b):
    """Compute n Chebyshev expansion coefficients of f on [a, b]."""
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
    b_next2, b_next1 = 0.0, 0.0
    for k in range(n - 1, 0, -1):
        b_k = coeffs[k] + 2.0 * t * b_next1 - b_next2
        b_next2 = b_next1
        b_next1 = b_k
    return coeffs[0] + t * b_next1 - b_next2


def _make_approx(f, degree, a, b):
    """Return a callable Chebyshev approximation of f on [a, b] of DEGREE `degree`.

    A degree-d polynomial has d+1 coefficients, so we request degree+1 of
    them.  This off-by-one is worth being pedantic about here: FHERMA scores
    on multiplicative depth, so mislabelling degree d-1 as d can make you
    report a depth you cannot actually achieve.

    On converting degree to depth: ceil(log2(degree+1)) is the
    Paterson-Stockmeyer *theoretical* cost, and OpenFHE's implementation
    charges more than that.  Use fherma_config.chebyshev_depth(), which
    encodes OpenFHE's published table -- a degree-7 fit costs 5 levels, not 3.
    """
    coeffs = _chebyshev_coefficients(f, degree + 1, a, b)
    return lambda x: _eval_chebyshev(coeffs, x, a, b)


def _max_error(f, approx_f, a, b, n_points=1000):
    """Maximum absolute error of approx_f vs f on a uniform grid."""
    worst = 0.0
    for i in range(n_points):
        x = a + (b - a) * i / (n_points - 1)
        err = abs(f(x) - approx_f(x))
        if err > worst:
            worst = err
    return worst


# ---------------------------------------------------------------------------
# Target activation functions
# ---------------------------------------------------------------------------

def sigmoid(x):
    """Standard sigmoid: 1 / (1 + exp(-x))."""
    # Numerically stable version
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    else:
        ex = math.exp(x)
        return ex / (1.0 + ex)


def relu(x):
    """Standard ReLU: max(0, x)."""
    return max(0.0, x)


def gelu(x):
    """Gaussian Error Linear Unit: x * Phi(x).

    Phi is the standard normal CDF. We use the exact form:
        GELU(x) = x * 0.5 * (1 + erf(x / sqrt(2)))
    """
    return x * 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


# ---------------------------------------------------------------------------
# Exercise functions
# ---------------------------------------------------------------------------

def evaluate_candidate(poly_fn, target_fn, domain, n_points=1000, max_depth=None):
    """Score a polynomial approximation against a target function.

    Parameters
    ----------
    poly_fn : callable
        The polynomial approximation.
    target_fn : callable
        The true activation function.
    domain : tuple(float, float)
        The interval [a, b].
    n_points : int
        Number of test points for error measurement.
    max_depth : int or None
        If provided, the maximum allowed multiplicative depth.
        (Not enforced here -- just recorded for reporting.)

    Returns
    -------
    dict
        {
            'max_error': float,
            'domain': tuple,
            'n_points': int,
            'max_depth': max_depth,
        }
    """
    a, b = domain
    max_err = _max_error(target_fn, poly_fn, a, b, n_points)
    return {
        "max_error": max_err,
        "domain": domain,
        "n_points": n_points,
        "max_depth": max_depth,
    }


def optimize_activation(target_fn, domain, min_degree=3, max_degree=25, max_error=0.1):
    """Find the lowest-degree Chebyshev approximation meeting an error threshold.

    Tries Chebyshev approximations at degrees min_degree, min_degree+1, ...,
    max_degree.  Returns the first degree whose max error on the domain is
    <= max_error.

    Parameters
    ----------
    target_fn : callable
        The true activation function.
    domain : tuple(float, float)
        The interval [a, b].
    min_degree : int
        Minimum polynomial degree to try.
    max_degree : int
        Maximum polynomial degree to try.
    max_error : float
        Accuracy threshold (maximum absolute error allowed).

    Returns
    -------
    dict
        {
            'optimal_degree': int or None,
            'max_error': float or None,
            'passes': bool,
            'search_log': list of (degree, max_error, passes) tuples,
        }
        If no degree in range meets the threshold, optimal_degree is None
        and passes is False.
    """
    a, b = domain
    search_log = []
    best_degree = None
    best_error = None

    for deg in range(min_degree, max_degree + 1):
        approx_fn = _make_approx(target_fn, deg, a, b)
        err = _max_error(target_fn, approx_fn, a, b, n_points=1000)
        passes = err <= max_error
        search_log.append((deg, err, passes))

        if passes and best_degree is None:
            best_degree = deg
            best_error = err

    return {
        "optimal_degree": best_degree,
        "max_error": best_error,
        "passes": best_degree is not None,
        "search_log": search_log,
    }


def challenge_relu(domain=(-5, 5), max_error=0.3):
    """Optimize a Chebyshev approximation of ReLU under FHERMA-like constraints.

    Returns
    -------
    dict
        Optimization result from optimize_activation.
    """
    return optimize_activation(relu, domain, min_degree=3, max_degree=25,
                               max_error=max_error)


def challenge_sigmoid(domain=(-8, 8), max_error=0.05):
    """Optimize a Chebyshev approximation of sigmoid under FHERMA-like constraints.

    Returns
    -------
    dict
        Optimization result from optimize_activation.
    """
    return optimize_activation(sigmoid, domain, min_degree=3, max_degree=25,
                               max_error=max_error)


def challenge_gelu(domain=(-5, 5), max_error=0.1):
    """Optimize a Chebyshev approximation of GELU under FHERMA-like constraints.

    Returns
    -------
    dict
        Optimization result from optimize_activation.
    """
    return optimize_activation(gelu, domain, min_degree=3, max_degree=25,
                               max_error=max_error)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
print("=== ex18: Activation Function Optimization (Capstone) ===\n")

# --- Test 1: evaluate_candidate works ---
approx_sig_11 = _make_approx(sigmoid, 11, -8, 8)
result = evaluate_candidate(approx_sig_11, sigmoid, (-8, 8))
print(f"  Sigmoid deg-11 candidate: max_error = {result['max_error']:.6f}")
check("evaluate_candidate returns max_error", "max_error" in result)

# --- Test 2: sigmoid optimization ---
print("\n  --- Sigmoid Challenge: [-8, 8], max_error = 0.05 ---")
sig_result = challenge_sigmoid()
check("sigmoid optimization found a solution", sig_result["passes"], True)
if sig_result["passes"]:
    print(f"  Optimal degree: {sig_result['optimal_degree']}")
    print(f"  Achieved error: {sig_result['max_error']:.6f}")
    check("sigmoid optimal degree <= 15", sig_result["optimal_degree"] <= 15)

# --- Test 3: ReLU optimization ---
print("\n  --- ReLU Challenge: [-5, 5], max_error = 0.3 ---")
relu_result = challenge_relu()
if relu_result["passes"]:
    print(f"  Optimal degree: {relu_result['optimal_degree']}")
    print(f"  Achieved error: {relu_result['max_error']:.6f}")
    check("ReLU optimization found a solution", relu_result["passes"], True)
else:
    print("  No solution found in degree range 3-25.")
    check("ReLU optimization found a solution", relu_result["passes"], True)

# --- Test 4: GELU optimization ---
print("\n  --- GELU Challenge: [-5, 5], max_error = 0.1 ---")
gelu_result = challenge_gelu()
if gelu_result["passes"]:
    print(f"  Optimal degree: {gelu_result['optimal_degree']}")
    print(f"  Achieved error: {gelu_result['max_error']:.6f}")
    check("GELU optimization found a solution", gelu_result["passes"], True)
else:
    print("  No solution found in degree range 3-25.")
    check("GELU optimization found a solution", gelu_result["passes"], True)

# --- Test 5: Full optimization report ---
print("\n  === Optimization Report ===")
print(f"  {'Activation':<12} {'Domain':<14} {'Threshold':<12} {'Degree':<8} "
      f"{'Max Error':<12} {'Status':<6}")
print("  " + "-" * 68)

for name, result, domain, threshold in [
    ("Sigmoid",  sig_result,  "[-8, 8]",  0.05),
    ("ReLU",     relu_result, "[-5, 5]",  0.30),
    ("GELU",     gelu_result, "[-5, 5]",  0.10),
]:
    if result["passes"]:
        print(f"  {name:<12} {domain:<14} {threshold:<12} "
              f"{result['optimal_degree']:<8} "
              f"{result['max_error']:<12.6f} {'PASS':<6}")
    else:
        print(f"  {name:<12} {domain:<14} {threshold:<12} "
              f"{'N/A':<8} {'N/A':<12} {'FAIL':<6}")

# --- Test 6: Print search log for sigmoid ---
print("\n  --- Sigmoid Search Log ---")
print(f"  {'Degree':>8}  {'Max Error':>12}  {'Passes':>6}")
print("  " + "-" * 30)
for deg, err, passes in sig_result["search_log"]:
    marker = " <-- optimal" if (sig_result["passes"] and
                                 deg == sig_result["optimal_degree"]) else ""
    print(f"  {deg:>8}  {err:>12.6f}  {'yes' if passes else 'no':>6}{marker}")
print("  " + "-" * 30)

# --- Test 7: turn the optimal degree into an actual submission config ------
# This is the step that closes the loop between "I found the cheapest degree"
# and "I declared parameters the evaluator will accept". The degree alone is
# not a submission -- mult_depth has to come from OpenFHE's real cost table,
# not from ceil(log2(degree+1)).
print("\n  --- From optimal degree to config.json ---")
try:
    from fherma_config import chebyshev_depth, naive_formula_depth, build_config, validate_config

    for name, res, rots in [("sigmoid", sig_result, [1, 2, 4]),
                            ("relu", relu_result, [1, 2, 4]),
                            ("gelu", gelu_result, [1, 2, 4])]:
        if not res["passes"]:
            continue
        deg = res["optimal_degree"]
        real = chebyshev_depth(deg)
        naive = naive_formula_depth(deg)
        cfg = build_config(mult_depth=real, rotation_indices=rots)
        print(f"  {name:<8} degree {deg:>2} -> depth {real} "
              f"(formula would say {naive}), N={cfg['ring_dimension']}")

    cfg = build_config(mult_depth=chebyshev_depth(sig_result["optimal_degree"]),
                       rotation_indices=[1, 2, 4])
    check("emitted config validates clean", validate_config(cfg), [])
    check("depth matches OpenFHE's table, not the formula",
          cfg["mult_depth"], chebyshev_depth(sig_result["optimal_degree"]))
except ImportError:
    print("  (fherma_config.py not importable -- run from tier4_fherma/)")

summary()
