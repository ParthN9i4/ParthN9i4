"""
Exercise 03 — Learning With Errors (LWE) Encryption

LWE is the computational hardness assumption behind most lattice-based
cryptography.  Given (A, b = A*s + e mod q) where e is "small" noise,
recovering s is believed to be hard.

This exercise builds a toy LWE encryption scheme:
  * Encrypt: hide a message m in Z_t inside b = a . s + e + floor(q/t)*m
  * Decrypt: compute (b - a . s) mod q, rescale to Z_t
  * Break:   show that when noise is too large, decryption fails

Parameters: n=8 (dimension), q=251 (modulus), t=4 (plaintext modulus).
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from check import check, summary
import numpy as np


# ---------------------------------------------------------------------------
# 1. Key generation
# ---------------------------------------------------------------------------

def keygen_lwe(n, q, rng=None):
    """Generate a secret key: a random vector s in Z_q^n.

    Parameters
    ----------
    n   : dimension of the secret vector
    q   : ciphertext modulus
    rng : numpy Generator (for reproducibility)

    Returns
    -------
    s : numpy array of shape (n,), dtype int64, entries in [0, q)
    """
    # === YOUR CODE HERE ===
    if rng is None:
        rng = np.random.default_rng()
    return rng.integers(0, q, size=n, dtype=np.int64)


# ---------------------------------------------------------------------------
# 2. Encryption
# ---------------------------------------------------------------------------

def encrypt_lwe(m, s, n, q, t, std, rng=None):
    """Encrypt a message m in Z_t under LWE.

    Steps:
      1. Sample a uniformly from Z_q^n.
      2. Sample noise e from a rounded Gaussian with standard deviation std.
      3. Compute b = (a . s + e + floor(q/t) * m) mod q.

    Returns (a, b) where a is shape (n,) and b is a scalar.
    """
    # === YOUR CODE HERE ===
    if rng is None:
        rng = np.random.default_rng()
    a = rng.integers(0, q, size=n, dtype=np.int64)
    e = int(round(rng.normal(0, std)))
    delta = q // t
    b = int((np.dot(a, s) + e + delta * m) % q)
    return a, b


# ---------------------------------------------------------------------------
# 3. Decryption
# ---------------------------------------------------------------------------

def decrypt_lwe(a, b, s, q, t):
    """Decrypt an LWE ciphertext (a, b) using secret key s.

    Steps:
      1. v = (b - a . s) mod q          — should be close to floor(q/t)*m
      2. m' = round(v * t / q) mod t     — rescale back to Z_t

    Returns the recovered plaintext in Z_t.
    """
    # === YOUR CODE HERE ===
    v = int((b - np.dot(a, s)) % q)
    m_dec = round(v * t / q) % t
    return m_dec


# ---------------------------------------------------------------------------
# 4. Demonstrate failure with large noise
# ---------------------------------------------------------------------------

def break_it_large_noise(s, n, q, t, rng=None):
    """Encrypt several random messages with huge noise (std = q // 4)
    and return the fraction of correct decryptions.

    This should be noticeably below 1.0 — large noise overwhelms the
    message encoding, making decryption unreliable.
    """
    # === YOUR CODE HERE ===
    if rng is None:
        rng = np.random.default_rng()
    big_std = q // 4
    trials = 200
    correct = 0
    for _ in range(trials):
        m = int(rng.integers(0, t))
        a, b = encrypt_lwe(m, s, n, q, t, big_std, rng)
        m_dec = decrypt_lwe(a, b, s, q, t)
        if m_dec == m:
            correct += 1
    return correct / trials


# ===================================================================
# Tests
# ===================================================================

if __name__ == "__main__":
    print("=== Ex03: LWE Encryption ===\n")

    n, q, t = 8, 251, 4
    std_small = 2

    rng = np.random.default_rng(seed=2024)
    s = keygen_lwe(n, q, rng)

    # --- Encrypt / decrypt round-trip with small noise ---
    all_ok = True
    for trial_m in range(t):
        a, b = encrypt_lwe(trial_m, s, n, q, t, std_small, rng)
        dec = decrypt_lwe(a, b, s, q, t)
        if dec != trial_m:
            all_ok = False
    check("encrypt/decrypt all messages 0..t-1", all_ok, True)

    # Many random messages
    correct = 0
    num_trials = 100
    for _ in range(num_trials):
        m = int(rng.integers(0, t))
        a, b = encrypt_lwe(m, s, n, q, t, std_small, rng)
        dec = decrypt_lwe(a, b, s, q, t)
        if dec == m:
            correct += 1
    check(f"100 random encrypt/decrypt (small noise): {correct}/100 correct",
          correct, 100)

    # --- Large noise breaks decryption ---
    rng_break = np.random.default_rng(seed=9999)
    s_break = keygen_lwe(n, q, rng_break)
    accuracy = break_it_large_noise(s_break, n, q, t, rng_break)
    print(f"\n  [info] Large-noise accuracy: {accuracy:.2%}")
    check("large noise accuracy < 90% (decryption is broken)",
          accuracy < 0.90, True)

    # --- Verify ciphertext structure ---
    rng2 = np.random.default_rng(seed=42)
    s2 = keygen_lwe(n, q, rng2)
    a, b = encrypt_lwe(0, s2, n, q, t, std_small, rng2)
    check("ciphertext 'a' has correct length", len(a), n)
    check("ciphertext 'b' is a scalar in [0, q)", 0 <= b < q, True)

    summary()
