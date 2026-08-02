"""
Exercise 01 — Modular Arithmetic, CRT, and the Number Theoretic Transform

Core building blocks for lattice-based cryptography:
  * Z_q arithmetic: add, multiply, inverse  (all ops stay in [0, q))
  * Chinese Remainder Theorem (CRT): reconstruct an integer from its
    residues modulo several co-prime moduli.
  * Number Theoretic Transform (NTT): the "integer FFT" that lets us
    multiply degree-(N-1) polynomials in O(N log N) over Z_q.

All polynomials are represented as numpy arrays of length N.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from check import check, summary
import numpy as np


# ---------------------------------------------------------------------------
# 1. Basic modular arithmetic
# ---------------------------------------------------------------------------

def mod_add(a, b, q):
    """Return (a + b) mod q."""
    # === YOUR CODE HERE ===
    return (a + b) % q


def mod_mul(a, b, q):
    """Return (a * b) mod q."""
    # === YOUR CODE HERE ===
    return (a * b) % q


def mod_inv(a, q):
    """Return the modular inverse of a mod q using the extended Euclidean algorithm.

    Raises ValueError if gcd(a, q) != 1.
    """
    # === YOUR CODE HERE ===
    def extended_gcd(a, b):
        if a == 0:
            return b, 0, 1
        g, x1, y1 = extended_gcd(b % a, a)
        return g, y1 - (b // a) * x1, x1

    a = a % q
    g, x, _ = extended_gcd(a, q)
    if g != 1:
        raise ValueError(f"No inverse: gcd({a}, {q}) = {g}")
    return x % q


# ---------------------------------------------------------------------------
# 2. Chinese Remainder Theorem
# ---------------------------------------------------------------------------

def crt_reconstruct(remainders, moduli):
    """Given remainders r_i and pairwise co-prime moduli m_i,
    return x such that x = r_i (mod m_i) for all i, with 0 <= x < M = prod(m_i).
    """
    # === YOUR CODE HERE ===
    M = 1
    for m in moduli:
        M *= m

    x = 0
    for r_i, m_i in zip(remainders, moduli):
        M_i = M // m_i
        y_i = mod_inv(M_i, m_i)
        x += r_i * M_i * y_i
    return x % M


# ---------------------------------------------------------------------------
# 3. Number Theoretic Transform (NTT)  —  Cooley-Tukey butterfly
# ---------------------------------------------------------------------------

def ntt(a, q, psi):
    """Compute the NTT of polynomial coefficient vector *a* in Z_q.

    Parameters
    ----------
    a   : array-like of length N (must be a power of 2)
    q   : prime modulus
    psi : a primitive 2N-th root of unity in Z_q
          (i.e. psi^N = -1 mod q, and no smaller power gives -1)

    Returns
    -------
    numpy array of length N — the NTT of a.

    Algorithm: iterative Cooley-Tukey decimation-in-time.
    The twiddle factor at stage s for group j is psi^(bit-reverse of j).
    We use the "negacyclic" NTT convention:
        A[k] = sum_{i=0}^{N-1} a[i] * psi^{(2*bit_rev(k)+1)*i}  mod q
    which is equivalent to pre-multiplying by powers of psi then doing a
    standard NTT.  Here we implement a simpler version using the butterfly.
    """
    # === YOUR CODE HERE ===
    N = len(a)
    A = np.array(a, dtype=np.int64) % q

    # Precompute powers of psi: psi^0, psi^1, ..., psi^{N-1}
    psi_powers = np.zeros(N, dtype=np.int64)
    psi_powers[0] = 1
    for i in range(1, N):
        psi_powers[i] = (psi_powers[i - 1] * psi) % q

    # Bit-reversal permutation
    log_n = int(np.log2(N))
    for i in range(N):
        j = int('{:0{width}b}'.format(i, width=log_n)[::-1], 2)
        if i < j:
            A[i], A[j] = A[j], A[i]

    # Cooley-Tukey butterfly
    length = 2
    while length <= N:
        half = length // 2
        step = N // length
        for i in range(0, N, length):
            for j in range(half):
                w = psi_powers[(j * step) % N]
                u = A[i + j]
                v = (A[i + j + half] * w) % q
                A[i + j] = (u + v) % q
                A[i + j + half] = (u - v) % q
        length *= 2

    return A % q


def intt(A, q, psi):
    """Compute the inverse NTT.

    Uses the fact that INTT is an NTT with psi replaced by psi^{-1},
    followed by multiplication by N^{-1} mod q.
    """
    # === YOUR CODE HERE ===
    N = len(A)
    psi_inv = mod_inv(psi, q)
    result = ntt(A, q, psi_inv)
    n_inv = mod_inv(N, q)
    return (result * n_inv) % q


# ===================================================================
# Tests
# ===================================================================

if __name__ == "__main__":
    print("=== Ex01: Modular Arithmetic, CRT, NTT ===\n")

    # --- mod_add ---
    check("mod_add(7, 5, 11)", mod_add(7, 5, 11), 1)
    check("mod_add(0, 0, 7)", mod_add(0, 0, 7), 0)
    check("mod_add(3, 4, 17)", mod_add(3, 4, 17), 7)

    # --- mod_mul ---
    check("mod_mul(3, 5, 7)", mod_mul(3, 5, 7), 1)
    check("mod_mul(6, 6, 17)", mod_mul(6, 6, 17), 2)

    # --- mod_inv ---
    check("mod_inv(3, 7) * 3 mod 7 == 1", mod_mul(mod_inv(3, 7), 3, 7), 1)
    check("mod_inv(5, 17) * 5 mod 17 == 1", mod_mul(mod_inv(5, 17), 5, 17), 1)
    check("mod_inv(2, 17)", mod_inv(2, 17), 9)  # 2*9=18=1 mod 17

    try:
        mod_inv(4, 8)
        check("mod_inv(4,8) should raise", False, True)
    except ValueError:
        check("mod_inv(4,8) raises ValueError", True, True)

    # --- CRT ---
    # x = 2 mod 3, x = 3 mod 5, x = 2 mod 7  =>  x = 23 mod 105
    check("CRT [2,3,2] mod [3,5,7]", crt_reconstruct([2, 3, 2], [3, 5, 7]), 23)
    # x = 1 mod 2, x = 2 mod 3, x = 3 mod 5  =>  x = 23 mod 30
    check("CRT [1,2,3] mod [2,3,5]", crt_reconstruct([1, 2, 3], [2, 3, 5]), 23)

    # --- NTT / INTT ---
    # q=17, psi=2 (2 is a primitive 8th root of unity mod 17: 2^4=16=-1 mod 17)
    q = 17
    psi = 2
    N = 4
    a = np.array([1, 2, 3, 4], dtype=np.int64)

    A = ntt(a, q, psi)
    a_recovered = intt(A, q, psi)

    check("NTT then INTT recovers original", list(a_recovered), list(a))

    # Verify NTT of [1,0,0,0] = [1,1,1,1] (all-ones, since it is the constant 1)
    one = np.array([1, 0, 0, 0], dtype=np.int64)
    One_ntt = ntt(one, q, psi)
    check("NTT of [1,0,0,0] is all ones", list(One_ntt), [1, 1, 1, 1])

    # Round-trip another vector
    b = np.array([5, 0, 12, 3], dtype=np.int64)
    check("INTT(NTT(b)) == b", list(intt(ntt(b, q, psi), q, psi)), list(b))

    summary()
