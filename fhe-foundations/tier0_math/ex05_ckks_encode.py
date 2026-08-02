"""
Exercise 05 — CKKS Encoding: from Complex Numbers to Polynomials

CKKS (Cheon-Kim-Kim-Song) is the FHE scheme for approximate arithmetic
on real/complex numbers.  Its magic is the *canonical embedding*:

  A polynomial m(X) of degree N-1 maps to N/2 complex "slots" by
  evaluating m at the primitive (2N)-th roots of unity.

Encoding workflow:
  complex vector z  -->  build conjugate-symmetric vector  -->  inverse
  Vandermonde (decode)  -->  scale and round  -->  integer polynomial

Decoding is the reverse: evaluate the polynomial at the roots, divide
by scale.  We use the Vandermonde matrix approach for clarity.

Parameters: N=8 (degree), so 4 complex slots; scale = 2^30.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from check import check, summary
import numpy as np


# ---------------------------------------------------------------------------
# 1. Roots of the 2N-th cyclotomic polynomial
# ---------------------------------------------------------------------------

def roots_of_cyclotomic(N):
    """Return the N/2 primitive (2N)-th roots of unity used by CKKS.

    These are omega^(2j+1) for j = 0, ..., N/2 - 1,
    where omega = exp(2*pi*i / (2N)).

    Returns a numpy complex128 array of length N/2.
    """
    # === YOUR CODE HERE ===
    M = 2 * N  # 2N
    omega = np.exp(2j * np.pi / M)
    half = N // 2
    roots = np.array([omega ** (2 * j + 1) for j in range(half)],
                     dtype=np.complex128)
    return roots


# ---------------------------------------------------------------------------
# 2. CKKS Encode: complex vector -> integer polynomial
# ---------------------------------------------------------------------------

def encode_ckks(z, N, scale):
    """Encode a complex vector z (length N/2) into an integer polynomial
    of degree N-1.

    Steps:
      (a) Build the full N-length vector by appending the conjugate of
          z in reverse order:  full = [z_0, z_1, ..., z_{N/2-1},
                                       conj(z_{N/2-1}), ..., conj(z_0)]
      (b) Construct the Vandermonde matrix V where V[i,j] = root_i^j
          using all N roots (the N/2 we picked + their conjugates).
          Actually, we need the full set of N roots: for CKKS these are
          omega^(2j+1) for j=0..N-1.  The first N/2 are our "slots",
          and the second N/2 are their conjugates.
      (c) Solve V @ m = full  for the polynomial coefficients m
          (equivalently, m = V^{-1} @ full).
      (d) Multiply by scale and round to nearest integer.

    Returns numpy int64 array of length N.
    """
    # === YOUR CODE HERE ===
    z = np.array(z, dtype=np.complex128)
    half = N // 2

    # (a) Build conjugate-symmetric vector of length N
    full = np.concatenate([z, np.conj(z[::-1])])

    # (b) All N roots: omega^(2j+1) for j = 0, ..., N-1
    M = 2 * N
    omega = np.exp(2j * np.pi / M)
    all_roots = np.array([omega ** (2 * j + 1) for j in range(N)],
                         dtype=np.complex128)

    # Vandermonde: V[i, j] = all_roots[i]^j
    V = np.vander(all_roots, N, increasing=True)

    # (c) Solve for polynomial coefficients
    m = np.linalg.solve(V, full)

    # (d) Scale and round
    # The result should be real (up to floating point noise)
    m_scaled = np.round(np.real(m * scale)).astype(np.int64)
    return m_scaled


# ---------------------------------------------------------------------------
# 3. CKKS Decode: integer polynomial -> complex vector
# ---------------------------------------------------------------------------

def decode_ckks(m, N, scale):
    """Decode an integer polynomial m (length N) back to N/2 complex values.

    Steps:
      (a) Get the N/2 roots (same as roots_of_cyclotomic).
      (b) Build Vandermonde V where V[i,j] = root_i^j, shape (N/2, N).
      (c) Evaluate: z = V @ m  (matrix-vector product).
      (d) Divide by scale.

    Returns numpy complex128 array of length N/2.
    """
    # === YOUR CODE HERE ===
    m = np.array(m, dtype=np.float64)
    half = N // 2

    roots = roots_of_cyclotomic(N)

    # Vandermonde: V[i, j] = roots[i]^j, shape (half, N)
    V = np.vander(roots, N, increasing=True)

    # Evaluate polynomial at roots
    z = V @ m

    # Divide by scale
    return z / scale


# ===================================================================
# Tests
# ===================================================================

if __name__ == "__main__":
    print("=== Ex05: CKKS Canonical Embedding Encode/Decode ===\n")

    N = 8        # polynomial degree bound
    half = N // 2  # = 4 complex slots
    scale = 2**30

    # --- roots_of_cyclotomic ---
    roots = roots_of_cyclotomic(N)
    check("number of roots", len(roots), half)

    # Each root should satisfy root^(2N) = 1  (it is a (2N)-th root of unity)
    powers_2N = roots ** (2 * N)
    all_near_one = np.allclose(powers_2N, 1.0)
    check("roots are (2N)-th roots of unity", all_near_one, True)

    # roots^N should be -1  (primitive: not an N-th root)
    powers_N = roots ** N
    all_near_neg_one = np.allclose(powers_N, -1.0)
    check("roots^N == -1 (primitive check)", all_near_neg_one, True)

    # --- encode then decode: real values ---
    z_real = np.array([3.14, -1.5, 2.71, 0.0], dtype=np.complex128)
    m_enc = encode_ckks(z_real, N, scale)
    z_dec = decode_ckks(m_enc, N, scale)

    # Should recover within a small tolerance (rounding introduces ~1/scale error)
    tol = 1e-3
    real_close = np.allclose(np.real(z_dec), np.real(z_real), atol=tol)
    check("encode/decode round-trip (real values)", real_close, True)

    # --- encode then decode: complex values ---
    z_complex = np.array([1 + 2j, -0.5 + 0.3j, 0.0 - 1j, 2.5 + 0j],
                         dtype=np.complex128)
    m_enc2 = encode_ckks(z_complex, N, scale)
    z_dec2 = decode_ckks(m_enc2, N, scale)

    complex_close = np.allclose(z_dec2, z_complex, atol=tol)
    check("encode/decode round-trip (complex values)", complex_close, True)

    # --- polynomial is integer-valued ---
    check("encoded polynomial is int64", m_enc.dtype, np.int64)

    # --- larger scale reduces error ---
    scale_small = 2**10
    scale_large = 2**40

    z_test = np.array([1.23456, -7.89012, 0.00001, 99.9],
                      dtype=np.complex128)

    m_small = encode_ckks(z_test, N, scale_small)
    z_small = decode_ckks(m_small, N, scale_small)
    err_small = np.max(np.abs(z_small - z_test))

    m_large = encode_ckks(z_test, N, scale_large)
    z_large = decode_ckks(m_large, N, scale_large)
    err_large = np.max(np.abs(z_large - z_test))

    print(f"\n  [info] Error with scale=2^10: {err_small:.6e}")
    print(f"  [info] Error with scale=2^40: {err_large:.6e}")
    check("larger scale gives smaller error", err_large < err_small, True)

    # --- slot independence ---
    # Encoding [1,0,0,0] and [0,0,0,1] should produce different polynomials
    z_slot0 = np.array([1, 0, 0, 0], dtype=np.complex128)
    z_slot3 = np.array([0, 0, 0, 1], dtype=np.complex128)
    m_slot0 = encode_ckks(z_slot0, N, scale)
    m_slot3 = encode_ckks(z_slot3, N, scale)
    check("different slots produce different polynomials",
          not np.array_equal(m_slot0, m_slot3), True)

    summary()
