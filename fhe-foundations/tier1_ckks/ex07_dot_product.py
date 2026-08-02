"""Exercise 07 -- Encrypted Dot Product (CKKS via TenSEAL)

The dot product is the foundation of linear algebra and, by extension,
machine learning.  In CKKS it is computed by:
  1. Element-wise multiplication of two encrypted vectors.
  2. Summing all slots (TenSEAL exposes this as enc.dot()).

Because CKKS is *approximate*, the encrypted result will differ slightly
from the plain computation.  We measure that error and verify it stays
well within acceptable bounds.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from check import check, summary

try:
    import tenseal as ts
    HAS_TENSEAL = True
except ImportError:
    HAS_TENSEAL = False
    print("TenSEAL not installed. Install with: pip install tenseal")
    print("Skipping exercises -- showing structure only.\n")


# ---------------------------------------------------------------------------
# Context setup
# ---------------------------------------------------------------------------
def make_context():
    ctx = ts.context(
        ts.SCHEME_TYPE.CKKS,
        poly_modulus_degree=8192,
        coeff_mod_bit_sizes=[60, 40, 40, 60],
    )
    ctx.global_scale = 2**40
    ctx.generate_galois_keys()
    return ctx


# ---------------------------------------------------------------------------
# Exercise functions
# ---------------------------------------------------------------------------
def encrypted_dot_product(ctx, a, b):
    """Encrypt both vectors, compute their dot product homomorphically,
    decrypt and return the scalar result."""
    enc_a = ts.ckks_vector(ctx, a)
    enc_b = ts.ckks_vector(ctx, b)
    enc_dot = enc_a.dot(enc_b)
    # dot() returns a CKKS vector with a single element
    return enc_dot.decrypt()[0]


def plain_dot_product(a, b):
    """Compute the dot product in plaintext for reference."""
    return sum(x * y for x, y in zip(a, b))


def measure_error(encrypted_result, plain_result):
    """Return the absolute difference between the two results."""
    return abs(encrypted_result - plain_result)


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
if HAS_TENSEAL:
    print("=== ex07: Encrypted Dot Product ===\n")

    ctx = make_context()

    vec_a = [1.5, 2.5, 3.5, 4.5]
    vec_b = [0.5, 1.0, 1.5, 2.0]

    # Plain reference: 1.5*0.5 + 2.5*1.0 + 3.5*1.5 + 4.5*2.0
    #                = 0.75 + 2.5 + 5.25 + 9.0 = 17.5
    plain_result = plain_dot_product(vec_a, vec_b)
    check("plain dot product", plain_result, 17.5, tol=1e-9)

    enc_result = encrypted_dot_product(ctx, vec_a, vec_b)
    error = measure_error(enc_result, plain_result)

    print(f"  INFO  encrypted result = {enc_result:.6f}")
    print(f"  INFO  plain result     = {plain_result:.6f}")
    print(f"  INFO  error            = {error:.2e}")

    check("encrypted dot product close to plain", enc_result, plain_result, tol=0.01)
    check("error below 0.01", error < 0.01, True)

    # --- second pair for variety ---
    vec_c = [1.0, 1.0, 1.0, 1.0]
    vec_d = [4.0, 3.0, 2.0, 1.0]
    plain2 = plain_dot_product(vec_c, vec_d)
    enc2 = encrypted_dot_product(ctx, vec_c, vec_d)
    check("dot([1,1,1,1], [4,3,2,1]) close to 10", enc2, plain2, tol=0.01)

summary()
