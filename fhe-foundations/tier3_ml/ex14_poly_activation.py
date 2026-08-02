"""Exercise 14 -- Chebyshev Polynomial Approximation of Activations

This is the single most important technique for FHE-friendly neural networks.
CKKS can only evaluate polynomials, so every non-polynomial activation (ReLU,
sigmoid, GELU, tanh, ...) must be replaced by a polynomial approximation.

Chebyshev polynomials are the gold standard because:
  1. They minimize the maximum error (minimax-like behaviour).
  2. Clenshaw recurrence evaluates them stably.
  3. Their coefficients are easy to compute via a discrete cosine transform
     at the Chebyshev nodes.

This exercise is pure NumPy -- no FHE library required.  The approximations
you build here plug directly into TenSEAL / OpenFHE workflows and into
FHERMA competition submissions.

Concepts
--------
* Chebyshev nodes:  x_k = (a+b)/2 + (b-a)/2 * cos((2k+1)*pi / (2n))
* Chebyshev coefficients via interpolation at nodes
* Clenshaw recurrence for stable evaluation
* Error analysis: max |f(x) - p(x)| over a test grid
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from check import check, summary

import math


# ---------------------------------------------------------------------------
# Exercise functions
# ---------------------------------------------------------------------------

def chebyshev_nodes(n, a=-1.0, b=1.0):
    """Return n Chebyshev nodes of the first kind on the interval [a, b].

    x_k = (a+b)/2 + (b-a)/2 * cos((2k+1) * pi / (2n)),  k = 0, ..., n-1

    These nodes cluster near the endpoints and minimise the interpolation
    error (Runge's phenomenon is avoided).
    """
    nodes = []
    for k in range(n):
        theta = (2 * k + 1) * math.pi / (2 * n)
        x_k = (a + b) / 2.0 + (b - a) / 2.0 * math.cos(theta)
        nodes.append(x_k)
    return nodes


def chebyshev_coefficients(f, n, a=-1.0, b=1.0):
    """Compute the first *n* Chebyshev expansion coefficients of f on [a, b].

    Uses the discrete orthogonality relation at n Chebyshev nodes:

        c_j = (2/n) * sum_{k=0}^{n-1} f(x_k) * cos(j * (2k+1) * pi / (2n))

    with c_0 halved (the 1/n convention).

    Parameters
    ----------
    f : callable
        The function to approximate.
    n : int
        Number of nodes / coefficients.
    a, b : float
        Interval endpoints.

    Returns
    -------
    list[float]
        Chebyshev coefficients c_0, c_1, ..., c_{n-1}.
    """
    nodes = chebyshev_nodes(n, a, b)
    f_vals = [f(x) for x in nodes]

    coeffs = []
    for j in range(n):
        s = 0.0
        for k in range(n):
            theta_k = (2 * k + 1) * math.pi / (2 * n)
            s += f_vals[k] * math.cos(j * theta_k)
        c_j = (2.0 / n) * s
        coeffs.append(c_j)
    # The zeroth coefficient uses 1/n, not 2/n -- equivalently halve it
    coeffs[0] /= 2.0
    return coeffs


def eval_chebyshev(coeffs, x, a=-1.0, b=1.0):
    """Evaluate a Chebyshev expansion at point x using Clenshaw recurrence.

    Maps x from [a, b] to t in [-1, 1], then applies:
        b_{n+1} = b_n = 0
        b_k = c_k + 2*t*b_{k+1} - b_{k+2}
        result = b_0 - t * b_1       (the Clenshaw identity for T_0 = 1)

    This is numerically stable and avoids computing T_k(x) explicitly.
    """
    # Map x to [-1, 1]
    t = (2.0 * x - (a + b)) / (b - a)

    n = len(coeffs)
    if n == 0:
        return 0.0
    if n == 1:
        return coeffs[0]

    # Clenshaw recurrence (backwards from k = n-1 down to k = 1)
    b_next2 = 0.0   # b_{k+2}
    b_next1 = 0.0   # b_{k+1}

    for k in range(n - 1, 0, -1):
        b_k = coeffs[k] + 2.0 * t * b_next1 - b_next2
        b_next2 = b_next1
        b_next1 = b_k

    # Final step: k = 0
    result = coeffs[0] + t * b_next1 - b_next2
    return result


def approx_relu(x, degree, a=-5.0, b=5.0):
    """Approximate ReLU(x) on [a, b] using a Chebyshev polynomial of given degree."""
    relu = lambda t: max(0.0, t)
    coeffs = chebyshev_coefficients(relu, degree, a, b)
    return eval_chebyshev(coeffs, x, a, b)


def approx_sigmoid(x, degree, a=-8.0, b=8.0):
    """Approximate sigmoid(x) on [a, b] using a Chebyshev polynomial of given degree."""
    sigmoid = lambda t: 1.0 / (1.0 + math.exp(-t))
    coeffs = chebyshev_coefficients(sigmoid, degree, a, b)
    return eval_chebyshev(coeffs, x, a, b)


def max_error(f, approx_f, a, b, n_test=1000):
    """Compute the maximum absolute error of approx_f vs f over n_test uniform points.

    Parameters
    ----------
    f : callable
        The true function.
    approx_f : callable
        The approximation (takes a single float argument).
    a, b : float
        Interval endpoints.
    n_test : int
        Number of test points.

    Returns
    -------
    float
        max |f(x) - approx_f(x)| over the test grid.
    """
    worst = 0.0
    for i in range(n_test):
        x = a + (b - a) * i / (n_test - 1)
        err = abs(f(x) - approx_f(x))
        if err > worst:
            worst = err
    return worst


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
print("=== ex14: Chebyshev Polynomial Activation Approximation ===\n")

# --- Test 1: Chebyshev nodes are in [a, b] ---
nodes = chebyshev_nodes(5, -1, 1)
check("nodes in [-1,1]", all(-1 <= x <= 1 for x in nodes))

# --- Test 2: Chebyshev approx of x^2 on [-1,1] with degree 3 is exact ---
# x^2 = (T_0(x) + T_2(x)) / 2, so degree-3 Chebyshev captures it exactly.
f_sq = lambda x: x ** 2
coeffs_sq = chebyshev_coefficients(f_sq, 3, -1, 1)
err_sq = max_error(f_sq, lambda x: eval_chebyshev(coeffs_sq, x, -1, 1), -1, 1)
print(f"  x^2 Chebyshev (deg 3) max error: {err_sq:.2e}")
check("x^2 approx exact at degree 3", err_sq < 1e-10)

# --- Test 3: Sigmoid error decreases with degree ---
sigmoid = lambda x: 1.0 / (1.0 + math.exp(-x))
err_5 = max_error(
    sigmoid,
    lambda x: approx_sigmoid(x, 5, -8, 8),
    -8, 8,
)
err_11 = max_error(
    sigmoid,
    lambda x: approx_sigmoid(x, 11, -8, 8),
    -8, 8,
)
print(f"  Sigmoid Chebyshev deg  5 max error: {err_5:.4f}")
print(f"  Sigmoid Chebyshev deg 11 max error: {err_11:.4f}")
check("sigmoid: deg-11 error < deg-5 error", err_11 < err_5)

# --- Test 4: ReLU approximation with degree 15 on [-5,5] ---
relu = lambda x: max(0.0, x)
err_relu_15 = max_error(
    relu,
    lambda x: approx_relu(x, 15, -5, 5),
    -5, 5,
)
print(f"  ReLU Chebyshev deg 15 on [-5,5] max error: {err_relu_15:.4f}")
check("ReLU deg-15 max error < 0.5", err_relu_15 < 0.5)

# --- Test 5: Table of degree vs max_error for sigmoid on [-8,8] ---
print("\n  Sigmoid on [-8, 8]: degree vs max error")
print("  " + "-" * 34)
print(f"  {'Degree':>8}  {'Max Error':>12}  {'< 0.1?':>6}")
print("  " + "-" * 34)
for deg in [3, 5, 7, 9, 11, 13, 15, 17, 19, 21]:
    e = max_error(
        sigmoid,
        lambda x, d=deg: approx_sigmoid(x, d, -8, 8),
        -8, 8,
    )
    flag = "yes" if e < 0.1 else "no"
    print(f"  {deg:>8}  {e:>12.6f}  {flag:>6}")
print("  " + "-" * 34)

# Verify the table shows convergence -- degree 21 should be quite accurate
err_21 = max_error(
    sigmoid,
    lambda x: approx_sigmoid(x, 21, -8, 8),
    -8, 8,
)
check("sigmoid deg-21 error < 0.01", err_21 < 0.01)

summary()
