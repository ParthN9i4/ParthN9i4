"""Exercise 13 -- Encrypted Logistic Regression Inference (TenSEAL CKKS)

Logistic regression is a natural fit for FHE because inference is a single
dot-product followed by a non-linear activation.  The weights and bias are
public; only the *input data* is encrypted -- the classic "ML-as-a-service"
threat model.

Key ideas
---------
* The sigmoid function is not polynomial, so we cannot evaluate it natively
  in CKKS.  We replace it with a degree-3 Maclaurin polynomial:

      sigmoid(x) ~ 0.5 + 0.197*x - 0.004*x^3

  This is accurate for |x| < ~4 and smooth enough for inference.
* The dot-product (X @ weights + bias) is a sequence of multiplications and
  additions on the ciphertext, then we apply the polynomial activation.
* The CKKS context must have enough *multiplicative depth* to handle the
  cubic term (x * x * x requires depth >= 3 after the initial matmul).
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from check import check, summary

import math

try:
    import tenseal as ts
    HAS_TENSEAL = True
except ImportError:
    HAS_TENSEAL = False
    print("TenSEAL not installed. Install with: pip install tenseal")
    print("Skipping TenSEAL exercises -- showing structure only.\n")

import random
random.seed(42)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def check_close(name, got, expected, tol=0.1):
    """Check that got is within tol of expected (scalar)."""
    ok = abs(got - expected) < tol
    check(name, ok, True)


# ---------------------------------------------------------------------------
# Exercise functions
# ---------------------------------------------------------------------------

def sigmoid_poly(x):
    """Degree-3 Maclaurin approximation of the sigmoid function.

    sigmoid(x) ~ 0.5 + 0.197*x - 0.004*x^3

    This is accurate for moderate |x| and avoids transcendentals so it can
    be evaluated homomorphically.
    """
    return 0.5 + 0.197 * x - 0.004 * (x ** 3)


def logistic_inference_plain(X, weights, bias):
    """Plain (unencrypted) logistic regression inference.

    Parameters
    ----------
    X : list[float]
        A single sample -- list of feature values.
    weights : list[float]
        Model weights (same length as X).
    bias : float
        Model bias scalar.

    Returns
    -------
    float
        Predicted probability via the polynomial sigmoid.
    """
    z = sum(x * w for x, w in zip(X, weights)) + bias
    return sigmoid_poly(z)


def logistic_inference_encrypted(ctx, X_enc, weights, bias):
    """Encrypted logistic regression inference using TenSEAL.

    The input *X_enc* is a CKKS-encrypted vector.  The weights and bias are
    plaintext -- we perform a plaintext-ciphertext dot product, add the bias,
    then apply the polynomial sigmoid on the ciphertext.

    Parameters
    ----------
    ctx : ts.Context
        TenSEAL CKKS context (unused directly but documents dependency).
    X_enc : ts.CKKSVector
        Encrypted input features.
    weights : list[float]
        Plaintext model weights.
    bias : float
        Plaintext model bias.

    Returns
    -------
    float
        Decrypted predicted probability.
    """
    # Dot product: element-wise multiply then sum
    z_enc = X_enc * weights           # element-wise ct * pt
    z_enc = z_enc.sum()               # sum slots -> scalar ciphertext
    z_enc = z_enc + bias              # add bias (plaintext scalar)

    # Polynomial sigmoid: 0.5 + 0.197*z - 0.004*z^3
    # Compute z^2 and z^3
    z2 = z_enc * z_enc                # z^2   (depth +1)
    z3 = z2 * z_enc                   # z^3   (depth +1)

    # 0.5 + 0.197*z - 0.004*z^3
    term1 = z_enc * 0.197             # 0.197*z
    term2 = z3 * (-0.004)             # -0.004*z^3
    result = term1 + term2 + 0.5      # combine

    # Decrypt -- result is a vector with one meaningful slot
    dec = result.decrypt()
    return dec[0]


# ---------------------------------------------------------------------------
# Context factory
# ---------------------------------------------------------------------------
def make_context():
    """Create a TenSEAL CKKS context with enough depth for logistic inference.

    We need depth for: matmul (1) + z^2 (1) + z^3 (1) = 3 multiplications,
    so we use a chain of 5 coefficient modulus primes (3 interior = 3 levels).
    """
    ctx = ts.context(
        ts.SCHEME_TYPE.CKKS,
        poly_modulus_degree=8192,
        coeff_mod_bit_sizes=[60, 40, 40, 40, 60],
    )
    ctx.global_scale = 2 ** 40
    ctx.generate_galois_keys()
    return ctx


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
print("=== ex13: Encrypted Logistic Regression ===\n")

# --- Test 1: sigmoid_poly sanity ---
check_close("sigmoid_poly(0) ~ 0.5", sigmoid_poly(0), 0.5, tol=1e-9)
check_close("sigmoid_poly(1) ~ 0.693", sigmoid_poly(1), 0.693, tol=0.01)
check("sigmoid_poly is monotone near 0",
      sigmoid_poly(-1) < sigmoid_poly(0) < sigmoid_poly(1))

# --- Test 2: plain inference ---
weights = [0.5, -0.3, 0.8, -0.2]
bias = 0.1
X = [1.0, 0.5, -0.5, 0.3]
plain_pred = logistic_inference_plain(X, weights, bias)
print(f"  Plain prediction: {plain_pred:.4f}")
check("plain prediction in [0, 1]", 0.0 <= plain_pred <= 1.0)

# --- Test 3: encrypted inference matches plain ---
if HAS_TENSEAL:
    ctx = make_context()
    X_enc = ts.ckks_vector(ctx, X)
    enc_pred = logistic_inference_encrypted(ctx, X_enc, weights, bias)
    print(f"  Encrypted prediction: {enc_pred:.4f}")
    check_close("encrypted ~ plain prediction", enc_pred, plain_pred, tol=0.1)

    # --- Test 4: different input ---
    X2 = [0.2, -0.7, 1.5, -1.0]
    plain_pred2 = logistic_inference_plain(X2, weights, bias)
    X2_enc = ts.ckks_vector(ctx, X2)
    enc_pred2 = logistic_inference_encrypted(ctx, X2_enc, weights, bias)
    print(f"  Plain prediction (X2):     {plain_pred2:.4f}")
    print(f"  Encrypted prediction (X2): {enc_pred2:.4f}")
    check_close("encrypted ~ plain (second input)", enc_pred2, plain_pred2, tol=0.1)

summary()
