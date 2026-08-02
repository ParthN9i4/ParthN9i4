"""Exercise 06 -- First Encryption (CKKS via TenSEAL)

Learn the core CKKS workflow:
  1. Create a TenSEAL context with CKKS parameters.
  2. Encrypt a plaintext vector into a CKKS ciphertext.
  3. Perform addition and multiplication on encrypted data.
  4. Decrypt and verify results match the expected plaintext computation.

CKKS works on *vectors of approximate real numbers*. Every operation
introduces a tiny amount of noise, so decrypted results are close to --
but not exactly equal to -- the plaintext answer.
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
# Helper: element-wise vector comparison via check()
# ---------------------------------------------------------------------------
def check_vec(name, got, expected, tol=0.01):
    """Compare two vectors element-wise within *tol* and report via check()."""
    ok = all(abs(a - b) < tol for a, b in zip(got, expected))
    check(name, ok, True)


# ---------------------------------------------------------------------------
# Context setup
# ---------------------------------------------------------------------------
def make_context():
    """Return a TenSEAL CKKS context with reasonable default parameters."""
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
def encrypt_vector(ctx, vec):
    """Encrypt a plain Python list of floats into a CKKS ciphertext vector."""
    return ts.ckks_vector(ctx, vec)


def add_encrypted(enc1, enc2):
    """Return the element-wise sum of two encrypted vectors."""
    return enc1 + enc2


def mul_encrypted(enc1, enc2):
    """Return the element-wise product of two encrypted vectors."""
    return enc1 * enc2


def add_plain(enc, plain_vec):
    """Add a plaintext vector to an encrypted vector."""
    return enc + plain_vec


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
if HAS_TENSEAL:
    print("=== ex06: First Encryption ===\n")

    ctx = make_context()

    # --- encrypt & decrypt round-trip ---
    vec_a = [1.0, 2.0, 3.0, 4.0]
    enc_a = encrypt_vector(ctx, vec_a)
    dec_a = enc_a.decrypt()
    check_vec("encrypt-decrypt round-trip", dec_a, vec_a, tol=0.01)

    # --- encrypted + encrypted ---
    vec_b = [10.0, 20.0, 30.0, 40.0]
    enc_b = encrypt_vector(ctx, vec_b)
    enc_sum = add_encrypted(enc_a, enc_b)
    dec_sum = enc_sum.decrypt()
    expected_sum = [11.0, 22.0, 33.0, 44.0]
    check_vec("enc + enc", dec_sum, expected_sum, tol=0.01)

    # --- encrypted + plaintext ---
    enc_a2 = encrypt_vector(ctx, vec_a)  # fresh ciphertext
    enc_add_plain = add_plain(enc_a2, vec_b)
    dec_add_plain = enc_add_plain.decrypt()
    check_vec("enc + plain", dec_add_plain, expected_sum, tol=0.01)

    # --- encrypted * encrypted ---
    vec_c = [2.0, 3.0, 4.0, 5.0]
    vec_d = [0.5, 1.0, 1.5, 2.0]
    enc_c = encrypt_vector(ctx, vec_c)
    enc_d = encrypt_vector(ctx, vec_d)
    enc_prod = mul_encrypted(enc_c, enc_d)
    dec_prod = enc_prod.decrypt()
    expected_prod = [a * b for a, b in zip(vec_c, vec_d)]
    check_vec("enc * enc", dec_prod, expected_prod, tol=0.01)

summary()
