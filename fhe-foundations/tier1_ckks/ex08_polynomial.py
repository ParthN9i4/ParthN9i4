"""Exercise 08 -- Polynomial Evaluation on Encrypted Data (CKKS)

Evaluating a polynomial  f(x) = a*x^2 + b*x + c  homomorphically is a
fundamental building block.  Activation functions, scoring models, and
many feature transforms can be approximated by low-degree polynomials.

Key insight -- and the one most people get wrong: in CKKS a multiplication
by a PLAINTEXT costs a level too, not just ciphertext x ciphertext.
Multiplying by a plaintext multiplies the scale (2^40 -> 2^80), so TenSEAL
must rescale afterwards, and a rescale drops one prime from the modulus
chain.  You can verify this yourself in a 1-level context ([60,40,60]):

    v = ts.ckks_vector(ctx, [1.0]); (v * 2.0)        # fine
                                    (v * 2.0) * 3.0  # ValueError: scale out of bounds

So "free" plaintext multiplies do not exist here.  Only ADDITION (of a
ciphertext or a plaintext) is depth-free.  Budget accordingly: the
depth of a circuit is its count of multiplications of ANY kind along the
longest path.

We compute the polynomial on an *entire vector at once* -- this is the
SIMD (single instruction, multiple data) nature of CKKS.

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

    We use HORNER form:  a*x^2 + b*x + c  =  (a*x + b)*x + c

    Depth accounting (remember: plaintext multiplies cost a level too):
        enc_x * a        -> level 1   (plaintext multiply, then rescale)
        + b              -> free      (addition never costs a level)
        * enc_x          -> level 2   (ciphertext multiply)
        + c              -> free
    Total depth 2, so the context needs at least 2 interior primes.

    Why Horner rather than the naive  a*(x*x) + b*x + c ?  The naive form
    also costs 2 levels, but it leaves you adding two ciphertexts that sit
    at DIFFERENT levels (a*x^2 at level 2, b*x at level 1), which is the
    single most common CKKS bug.  Horner keeps one running accumulator, so
    every operand is always at the same level by construction.
    """
    enc_x = ts.ckks_vector(ctx, x_vec)

    # (a*x + b)              -- one plaintext multiply (costs a level), then
    #                           a depth-free plaintext addition
    acc = enc_x * a + b

    # (a*x + b) * x + c      -- one ciphertext multiply, then a free addition
    acc = acc * enc_x + c

    return acc.decrypt()


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
