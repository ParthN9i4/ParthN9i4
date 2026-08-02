"""Exercise 08 -- Polynomial Evaluation on Encrypted Data (CKKS)

Evaluating a polynomial  f(x) = a*x^2 + b*x + c  homomorphically is a
fundamental building block.  Activation functions, scoring models, and
many feature transforms can be approximated by low-degree polynomials.

Key insight: every ciphertext multiplication consumes one *multiplicative
level*.  A degree-2 polynomial needs at least 2 levels (one for x^2, one
for a*x^2).  The context below is configured with enough depth for this.

We compute the polynomial on an *entire vector at once* -- this is the
SIMD (single instruction, multiple data) nature of CKKS.
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
# Context setup (enough depth for degree-2 polynomial)
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
def eval_poly_plain(x_vec, a, b, c):
    """Evaluate  a*x^2 + b*x + c  element-wise on a plain vector."""
    return [a * x * x + b * x + c for x in x_vec]


def eval_poly_encrypted(ctx, x_vec, a, b, c):
    """Encrypt x_vec, evaluate  a*x^2 + b*x + c  homomorphically,
    then decrypt and return the result list.

    Strategy (minimises depth):
        term2 = enc_x * enc_x          # depth 1  (x^2)
        term2 = term2 * a              # plain mul, no extra depth
        term1 = enc_x * b              # plain mul, depth 0
        term0 = c                      # constant
        result = term2 + term1 + c     # additions are free in depth
    """
    enc_x = ts.ckks_vector(ctx, x_vec)

    # x^2  (consumes 1 multiplicative level)
    enc_x2 = enc_x * enc_x

    # a * x^2  (plain scalar multiply -- free in depth)
    enc_ax2 = enc_x2 * a

    # b * x  (plain scalar multiply)
    enc_bx = enc_x * b

    # a*x^2 + b*x + c
    result = enc_ax2 + enc_bx + c

    return result.decrypt()


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
if HAS_TENSEAL:
    print("=== ex08: Polynomial Evaluation ===\n")

    ctx = make_context()

    # f(x) = 2x^2 + 3x + 1
    a, b, c = 2.0, 3.0, 1.0
    x_vec = [0.5, 1.0, 1.5, 2.0]

    plain_result = eval_poly_plain(x_vec, a, b, c)
    # Expected: [2*0.25+1.5+1, 2*1+3+1, 2*2.25+4.5+1, 2*4+6+1]
    #         = [3.0,          6.0,      10.0,          15.0]
    check("plain poly [0.5]", plain_result[0], 3.0, tol=1e-9)
    check("plain poly [1.0]", plain_result[1], 6.0, tol=1e-9)
    check("plain poly [1.5]", plain_result[2], 10.0, tol=1e-9)
    check("plain poly [2.0]", plain_result[3], 15.0, tol=1e-9)

    enc_result = eval_poly_encrypted(ctx, x_vec, a, b, c)

    print(f"  INFO  plain:     {plain_result}")
    print(f"  INFO  encrypted: {[round(v, 4) for v in enc_result]}")

    check("enc poly matches plain", enc_result, plain_result, tol=0.1)

    # --- second polynomial: -x^2 + 4x - 3 ---
    a2, b2, c2 = -1.0, 4.0, -3.0
    x_vec2 = [1.0, 2.0, 3.0]
    plain2 = eval_poly_plain(x_vec2, a2, b2, c2)
    enc2 = eval_poly_encrypted(ctx, x_vec2, a2, b2, c2)
    check("enc poly2 matches plain", enc2, plain2, tol=0.1)

summary()
