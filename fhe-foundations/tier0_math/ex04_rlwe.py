"""
Exercise 04 — Ring-LWE Encryption with Homomorphic Addition

RLWE moves from vectors (LWE) to polynomials in R_q = Z_q[X]/(X^N+1).
This gives us:
  * Compact keys (one polynomial instead of a matrix row)
  * Efficient operations via NTT
  * Homomorphic addition: adding ciphertexts = adding plaintexts

Ciphertexts are pairs (c0, c1) in R_q x R_q.
Decrypt: v = c0 + c1*s mod q, then rescale each coefficient to Z_t.

Parameters: N=16, q=32749 (prime), t=16 (plaintext modulus), std=2.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from check import check, summary
import numpy as np


# ---------------------------------------------------------------------------
# Polynomial helpers (self-contained so this file runs standalone)
# ---------------------------------------------------------------------------

def _poly_mod(p, N, q):
    """Reduce polynomial p modulo (X^N + 1) and mod q."""
    p = np.array(p, dtype=np.int64)
    result = np.zeros(N, dtype=np.int64)
    for i, c in enumerate(p):
        pos = i % N
        sign = (-1) ** (i // N)
        result[pos] += sign * c
    return result % q


def _poly_add(a, b, N, q):
    """Add two polynomials in R_q."""
    return (np.array(a, dtype=np.int64) + np.array(b, dtype=np.int64)) % q


def _poly_mul(a, b, N, q):
    """Schoolbook multiply in R_q (negacyclic convolution)."""
    a = np.array(a, dtype=np.int64)
    b = np.array(b, dtype=np.int64)
    full = np.convolve(a, b)
    result = np.zeros(N, dtype=np.int64)
    for i, c in enumerate(full):
        pos = i % N
        sign = (-1) ** (i // N)
        result[pos] += sign * c
    return result % q


# ---------------------------------------------------------------------------
# 1. Key generation
# ---------------------------------------------------------------------------

def keygen_rlwe(N, q, rng=None):
    """Generate a secret key: polynomial s with small coefficients in {-1, 0, 1}.

    Returns s as numpy array of length N.
    """
    # === YOUR CODE HERE ===
    if rng is None:
        rng = np.random.default_rng()
    s = rng.integers(-1, 2, size=N, dtype=np.int64)  # values in {-1, 0, 1}
    return s % q  # store in [0, q)


# ---------------------------------------------------------------------------
# 2. Encryption
# ---------------------------------------------------------------------------

def encrypt_rlwe(m, s, N, q, t, std, rng=None):
    """Encrypt a message polynomial m (coefficients in Z_t) under RLWE.

    Steps:
      1. a = random polynomial in R_q
      2. e = noise polynomial (rounded Gaussian, std=std)
      3. delta = floor(q / t)
      4. c1 = a                                        (in R_q)
      5. c0 = -(a*s + e) + delta*m   mod q             (in R_q)

    Returns (c0, c1) — both numpy arrays of length N.
    """
    # === YOUR CODE HERE ===
    if rng is None:
        rng = np.random.default_rng()
    m = np.array(m, dtype=np.int64)
    a = rng.integers(0, q, size=N, dtype=np.int64)
    e = np.round(rng.normal(0, std, size=N)).astype(np.int64)
    delta = q // t

    # c0 = -(a*s + e) + delta*m  mod q
    as_prod = _poly_mul(a, s, N, q)
    c0 = (-(as_prod + e) + delta * m) % q
    c1 = a.copy()
    return c0, c1


# ---------------------------------------------------------------------------
# 3. Decryption
# ---------------------------------------------------------------------------

def decrypt_rlwe(ct, s, N, q, t):
    """Decrypt an RLWE ciphertext (c0, c1).

    Steps:
      1. v = (c0 + c1 * s) mod q       — gives  delta*m + e'
      2. For each coefficient: m_i = round(v_i * t / q) mod t

    Returns numpy array of length N (recovered message polynomial in Z_t).
    """
    # === YOUR CODE HERE ===
    c0, c1 = ct
    v = _poly_add(c0, _poly_mul(c1, s, N, q), N, q)

    # Rescale each coefficient: round(v_i * t / q) mod t
    # Need to handle the centered representation for rounding
    m_dec = np.zeros(N, dtype=np.int64)
    for i in range(N):
        vi = int(v[i])
        m_dec[i] = round(vi * t / q) % t
    return m_dec


# ---------------------------------------------------------------------------
# 4. Homomorphic addition
# ---------------------------------------------------------------------------

def add_rlwe(ct1, ct2, N, q):
    """Add two RLWE ciphertexts component-wise.

    If ct1 encrypts m1 and ct2 encrypts m2, the result encrypts m1+m2 (mod t)
    — provided the accumulated noise stays small.
    """
    # === YOUR CODE HERE ===
    c0_1, c1_1 = ct1
    c0_2, c1_2 = ct2
    c0 = _poly_add(c0_1, c0_2, N, q)
    c1 = _poly_add(c1_1, c1_2, N, q)
    return c0, c1


# ---------------------------------------------------------------------------
# 5. Noise visualization
# ---------------------------------------------------------------------------

def visualize_noise(ct, s, m, N, q, t):
    """Compute the noise in a ciphertext and return the max absolute coefficient.

    noise = (c0 + c1*s) - delta*m   (mod q, centered in [-q/2, q/2))

    Returns the maximum |noise_i| across all coefficients.
    """
    # === YOUR CODE HERE ===
    c0, c1 = ct
    m = np.array(m, dtype=np.int64)
    delta = q // t

    v = _poly_add(c0, _poly_mul(c1, s, N, q), N, q)
    noise = (v - delta * m) % q

    # Center into [-q/2, q/2)
    noise = np.where(noise > q // 2, noise - q, noise)
    return int(np.max(np.abs(noise)))


# ===================================================================
# Tests
# ===================================================================

if __name__ == "__main__":
    print("=== Ex04: RLWE Encryption + Homomorphic Addition ===\n")

    N, q, t, std = 16, 32749, 16, 2
    rng = np.random.default_rng(seed=2024)

    s = keygen_rlwe(N, q, rng)

    # --- Encrypt / decrypt round-trip ---
    m1 = rng.integers(0, t, size=N, dtype=np.int64)
    ct1 = encrypt_rlwe(m1, s, N, q, t, std, rng)
    m1_dec = decrypt_rlwe(ct1, s, N, q, t)
    check("encrypt/decrypt round-trip", list(m1_dec), list(m1))

    # Another message
    m2 = rng.integers(0, t, size=N, dtype=np.int64)
    ct2 = encrypt_rlwe(m2, s, N, q, t, std, rng)
    m2_dec = decrypt_rlwe(ct2, s, N, q, t)
    check("encrypt/decrypt second message", list(m2_dec), list(m2))

    # --- Homomorphic addition ---
    ct_sum = add_rlwe(ct1, ct2, N, q)
    m_sum_dec = decrypt_rlwe(ct_sum, s, N, q, t)
    m_sum_expected = (m1 + m2) % t
    check("homomorphic addition: Dec(ct1+ct2) == m1+m2 mod t",
          list(m_sum_dec), list(m_sum_expected))

    # --- Multiple additions ---
    m3 = rng.integers(0, t, size=N, dtype=np.int64)
    ct3 = encrypt_rlwe(m3, s, N, q, t, std, rng)
    ct_triple = add_rlwe(add_rlwe(ct1, ct2, N, q), ct3, N, q)
    m_triple_dec = decrypt_rlwe(ct_triple, s, N, q, t)
    m_triple_expected = (m1 + m2 + m3) % t
    check("triple addition: Dec(ct1+ct2+ct3) == m1+m2+m3 mod t",
          list(m_triple_dec), list(m_triple_expected))

    # --- Noise ---
    noise_fresh = visualize_noise(ct1, s, m1, N, q, t)
    noise_sum = visualize_noise(ct_sum, s, m_sum_expected, N, q, t)
    print(f"\n  [info] Fresh ciphertext max noise:  {noise_fresh}")
    print(f"  [info] After addition max noise:    {noise_sum}")
    check("fresh noise is small (< q/2t)",
          noise_fresh < q // (2 * t), True)
    check("noise grows after addition",
          noise_sum >= noise_fresh, True)

    # --- Zero message ---
    m_zero = np.zeros(N, dtype=np.int64)
    ct_zero = encrypt_rlwe(m_zero, s, N, q, t, std, rng)
    m_zero_dec = decrypt_rlwe(ct_zero, s, N, q, t)
    check("encrypt/decrypt zero message", list(m_zero_dec), list(m_zero))

    summary()
