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

def ntt(a, q, w):
    """Compute the CYCLIC NTT of coefficient vector *a* in Z_q.

    This is the transform that diagonalizes multiplication modulo X^N - 1:
        A[k] = sum_{i=0}^{N-1} a[i] * w^{i k}   mod q

    Parameters
    ----------
    a : array-like of length N (must be a power of 2)
    q : prime modulus
    w : a primitive N-th root of unity in Z_q.  Concretely this means
        w^N = 1 and w^{N/2} = -1 mod q.  (The second condition is what
        makes the butterfly split correctly at every stage; a value with
        w^N = -1 is a 2N-th root and will NOT work here.)

    Returns
    -------
    numpy array of length N — the cyclic NTT of a.

    IMPORTANT — cyclic vs negacyclic.  Lattice crypto works in
    R_q = Z_q[X]/(X^N + 1), which needs the *negacyclic* convolution, NOT
    the cyclic one computed here.  Conflating the two is the classic
    implementation bug in this area.  The bridge is the "psi-twist": given
    psi a primitive 2N-th root (psi^N = -1), pre-multiply by psi^i, run
    this cyclic NTT with w = psi^2, and post-multiply by psi^{-i}.
    ex02_ring_poly.poly_mul_ntt does exactly that — see it for the full
    negacyclic multiplication.

    Algorithm: iterative Cooley-Tukey decimation-in-time.
    """
    # === YOUR CODE HERE ===
    N = len(a)
    A = np.array(a, dtype=np.int64) % q
    if pow(int(w), N, q) != 1 or pow(int(w), N // 2, q) != q - 1:
        raise ValueError(
            f"w={w} is not a primitive {N}-th root of unity mod {q}: "
            f"need w^{N}=1 and w^{N//2}=-1, got {pow(int(w), N, q)} and "
            f"{pow(int(w), N // 2, q)}"
        )

    # Precompute powers of w: w^0, w^1, ..., w^{N-1}
    w_powers = np.zeros(N, dtype=np.int64)
    w_powers[0] = 1
    for i in range(1, N):
        w_powers[i] = (w_powers[i - 1] * w) % q

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
                tw = w_powers[(j * step) % N]
                u = A[i + j]
                v = (A[i + j + half] * tw) % q
                A[i + j] = (u + v) % q
                A[i + j + half] = (u - v) % q
        length *= 2

    return A % q


def intt(A, q, w):
    """Compute the inverse cyclic NTT.

    Uses the fact that the INTT is an NTT with w replaced by w^{-1},
    followed by multiplication by N^{-1} mod q.  (w^{-1} is again a
    primitive N-th root, so the validity check in ntt still passes.)
    """
    # === YOUR CODE HERE ===
    N = len(A)
    w_inv = mod_inv(w, q)
    result = ntt(A, q, w_inv)
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
    # q=17, N=4.  We need a primitive *N*-th = 4th root of unity: w^4 = 1
    # and w^2 = -1.  That is w = 4  (4^2 = 16 = -1 mod 17, 4^4 = 1).
    #
    # Careful: psi = 2 is a primitive *8th* root mod 17 (2^4 = 16 = -1), so
    # it is the right value for the negacyclic TWIST in ex02, but it is NOT
    # a valid root for this cyclic transform.  The check inside ntt() now
    # rejects it rather than silently computing a meaningless matrix.
    q = 17
    N = 4
    w = 4
    a = np.array([1, 2, 3, 4], dtype=np.int64)

    A = ntt(a, q, w)
    a_recovered = intt(A, q, w)

    check("NTT then INTT recovers original", list(a_recovered), list(a))

    # NTT of the constant polynomial 1 evaluates to 1 at every point.
    one = np.array([1, 0, 0, 0], dtype=np.int64)
    check("NTT of [1,0,0,0] is all ones", list(ntt(one, q, w)), [1, 1, 1, 1])

    # Round-trip another vector
    b = np.array([5, 0, 12, 3], dtype=np.int64)
    check("INTT(NTT(b)) == b", list(intt(ntt(b, q, w), q, w)), list(b))

    # A wrong root must be rejected, not silently accepted.
    try:
        ntt(a, q, 2)
        check("ntt rejects psi=2 (a 2N-th root)", False, True)
    except ValueError:
        check("ntt rejects psi=2 (a 2N-th root)", True, True)

    # --- NON-VACUOUS test: the NTT must actually diagonalize CYCLIC
    # convolution.  A round-trip test alone would pass even if the
    # transform were nonsense, so we check it against a direct
    # convolution computed independently.
    def cyclic_conv(x, y, N, q):
        out = np.zeros(N, dtype=np.int64)
        for i in range(N):
            for j in range(N):
                out[(i + j) % N] = (out[(i + j) % N] + x[i] * y[j]) % q
        return out

    rng = np.random.default_rng(0)
    ok = True
    for _ in range(20):
        x = rng.integers(0, q, N)
        y = rng.integers(0, q, N)
        via_ntt = intt((ntt(x, q, w) * ntt(y, q, w)) % q, q, w)
        if list(via_ntt) != list(cyclic_conv(x, y, N, q)):
            ok = False
            break
    check("pointwise NTT product == cyclic convolution (20 random pairs)", ok, True)

    summary()
