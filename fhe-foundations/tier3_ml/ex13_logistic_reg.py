"""Exercise 13 -- Encrypted Logistic Regression Inference (TenSEAL CKKS)

Logistic regression is a natural fit for FHE because inference is a single
dot-product followed by a non-linear activation.  The weights and bias are
public; only the *input data* is encrypted -- the classic "ML-as-a-service"
threat model.

Key ideas
---------
* The sigmoid function is not polynomial, so we cannot evaluate it natively
  in CKKS.  We replace it with a degree-3 LEAST-SQUARES fit:

      sigmoid(x) ~ 0.5 + 0.197*x - 0.004*x^3        (max error ~0.05 on [-5,5])

  This is NOT the Maclaurin series.  The degree-3 Maclaurin expansion is
  0.5 + 0.25*x - x^3/48, and it is far worse away from the origin (max
  error 0.82 on [-4,4], 1.85 on [-5,5]) because Taylor expansions optimise
  accuracy at a single point, while least-squares/minimax fits spread the
  error across the whole interval.  That distinction is the entire reason
  the FHE-ML literature uses fitted polynomials rather than Taylor ones.
  (Verify: an L2 fit of 0.5 + a*x + b*x^3 to sigmoid over [-5,5] returns
  a = 0.1983, b = -0.00447.  The other widely cited variant, fitted over
  [-8,8] by Kim et al. 2018, is 0.5 + 0.15*x - 0.0015*x^3.)
* The dot-product (X @ weights + bias) is a sequence of multiplications and
  additions on the ciphertext, then we apply the polynomial activation.
* Depth: remember that plaintext multiplies consume a level too (ex08), so
  count EVERY multiplication.  See make_context below for the accounting.
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
    """Degree-3 least-squares approximation of the sigmoid function on [-5,5].

    sigmoid(x) ~ 0.5 + 0.197*x - 0.004*x^3

    Accurate to ~0.05 on [-5,5]; it diverges badly outside that range (the
    cubic term takes over), so in a real pipeline you must bound the
    pre-activation z -- e.g. by scaling the inputs -- before applying it.
    Not a Taylor/Maclaurin series: see the module docstring.
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
    z_enc = X_enc * weights           # element-wise ct * pt   -> level 1
    z_enc = z_enc.sum()               # sum slots (rotations; costs no level)
    z_enc = z_enc + bias              # add bias -- additions are free

    # Polynomial sigmoid in HORNER form:
    #     0.5 + 0.197*z - 0.004*z^3  =  0.5 + z * (0.197 - 0.004*z^2)
    #
    # Writing it this way keeps one accumulator, so we never add two
    # ciphertexts sitting at different levels (the classic CKKS bug that
    # the naive term-by-term version walks straight into).
    z2 = z_enc * z_enc                # z^2                       -> level 2
    inner = z2 * (-0.004) + 0.197     # 0.197 - 0.004*z^2         -> level 3
    result = inner * z_enc + 0.5      # z*(...) + 0.5             -> level 4

    # Decrypt -- result is a vector with one meaningful slot
    dec = result.decrypt()
    return dec[0]


# ---------------------------------------------------------------------------
# Context factory
# ---------------------------------------------------------------------------
def make_context():
    """Create a TenSEAL CKKS context with enough depth for logistic inference.

    Depth accounting (every multiplication counts, plaintext ones included):
        1. X * weights          (ct * pt)
        2. z * z                (ct * ct)
        3. z2 * (-0.004)        (ct * pt)  <-- easy to forget
        4. inner * z            (ct * ct)
    That is 4 levels, so we need 4 interior primes:
    len(coeff_mod_bit_sizes) - 2 = 4.

    Ring size: the chain below totals 60+40*4+60 = 280 bits.  SEAL caps the
    coefficient modulus at 218 bits for N=8192 at the default 128-bit
    security level (per the HomomorphicEncryption.org standard), so N=8192
    would raise "encryption parameters are not set correctly".  N=16384
    allows up to 438 bits and is the smallest ring that fits this circuit.
    """
    ctx = ts.context(
        ts.SCHEME_TYPE.CKKS,
        poly_modulus_degree=16384,
        coeff_mod_bit_sizes=[60, 40, 40, 40, 40, 60],
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
