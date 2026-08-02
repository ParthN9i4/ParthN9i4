"""
Exercise 02 — Polynomial Arithmetic in R_q = Z_q[X]/(X^N + 1)

The ring R_q is the quotient ring of polynomials with coefficients in Z_q
reduced modulo the cyclotomic polynomial X^N + 1 (N a power of 2).

Key insight: X^N = -1 in this ring, so any power X^{N+k} wraps around
as -X^k.  This "negacyclic" reduction is what makes the ring structured
enough for efficient crypto yet hard enough for security.

Polynomials are represented as numpy int64 arrays of length N:
  p = [a_0, a_1, ..., a_{N-1}]  means  a_0 + a_1*X + ... + a_{N-1}*X^{N-1}.
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from check import check, summary
import numpy as np

# We can import NTT/INTT from ex01 for the NTT-based multiplication.
from ex01_modular_arith import ntt, intt, mod_inv


# ---------------------------------------------------------------------------
# 1. Polynomial reduction modulo (X^N + 1, q)
# ---------------------------------------------------------------------------

def poly_mod(p, N, q):
    """Reduce polynomial p modulo (X^N + 1) and then modulo q.

    p may have degree >= N.  Because X^N = -1, each coefficient at
    position i >= N wraps: coeff at (i mod N) gets -= coeff at i,
    effectively applying the negacyclic folding.

    Returns numpy array of length N with coefficients in [0, q).
    """
    # === YOUR CODE HERE ===
    p = np.array(p, dtype=np.int64)
    result = np.zeros(N, dtype=np.int64)
    for i, c in enumerate(p):
        pos = i % N
        sign = (-1) ** (i // N)
        result[pos] += sign * c
    return result % q


# ---------------------------------------------------------------------------
# 2. Addition in R_q
# ---------------------------------------------------------------------------

def poly_add(a, b, N, q):
    """Add two polynomials in R_q = Z_q[X]/(X^N+1).

    Both a, b should be arrays of length N.
    Returns array of length N with coefficients in [0, q).
    """
    # === YOUR CODE HERE ===
    a = np.array(a, dtype=np.int64)
    b = np.array(b, dtype=np.int64)
    return (a + b) % q


# ---------------------------------------------------------------------------
# 3. Schoolbook multiplication in R_q
# ---------------------------------------------------------------------------

def poly_mul_schoolbook(a, b, N, q):
    """Multiply two polynomials in R_q using the schoolbook method.

    1. Compute the full product (degree up to 2N-2).
    2. Reduce modulo (X^N + 1): for each term c_k * X^k with k >= N,
       subtract c_k from coefficient at position k - N (negacyclic wrap).
    3. Reduce coefficients modulo q.

    Returns numpy array of length N.
    """
    # === YOUR CODE HERE ===
    a = np.array(a, dtype=np.int64)
    b = np.array(b, dtype=np.int64)

    # Full convolution (length 2N - 1)
    full = np.convolve(a, b)

    # Negacyclic reduction: X^N = -1, so X^{N+k} = -X^k
    result = np.zeros(N, dtype=np.int64)
    for i, c in enumerate(full):
        pos = i % N
        sign = (-1) ** (i // N)
        result[pos] += sign * c

    return result % q


# ---------------------------------------------------------------------------
# 4. NTT-based multiplication in R_q
# ---------------------------------------------------------------------------

def poly_mul_ntt(a, b, N, q, psi):
    """Multiply two polynomials in R_q using the Number Theoretic Transform.

    The NTT from ex01 computes a *cyclic* convolution (mod X^N - 1).
    To get a *negacyclic* convolution (mod X^N + 1) we apply the
    standard "twist":

      1. Pre-multiply:  a'[i] = a[i] * psi^i,  b'[i] = b[i] * psi^i
      2. Forward NTT of a' and b' (using psi^2 as the N-th root of unity).
      3. Point-wise multiply in NTT domain.
      4. Inverse NTT of the product.
      5. Post-multiply: c[i] = c'[i] * psi^{-i}

    Parameters
    ----------
    psi : primitive 2N-th root of unity mod q  (psi^N = -1 mod q)

    Returns numpy array of length N.
    """
    # === YOUR CODE HERE ===
    a = np.array(a, dtype=np.int64) % q
    b = np.array(b, dtype=np.int64) % q

    # Precompute powers of psi: psi^0, psi^1, ..., psi^{N-1}
    psi_powers = np.zeros(N, dtype=np.int64)
    psi_powers[0] = 1
    for i in range(1, N):
        psi_powers[i] = (psi_powers[i - 1] * psi) % q

    # Precompute inverse powers of psi
    psi_inv = mod_inv(psi, q)
    psi_inv_powers = np.zeros(N, dtype=np.int64)
    psi_inv_powers[0] = 1
    for i in range(1, N):
        psi_inv_powers[i] = (psi_inv_powers[i - 1] * psi_inv) % q

    # psi^2 is a primitive N-th root of unity (for the standard NTT)
    psi2 = (psi * psi) % q

    # Step 1: twist inputs
    a_twisted = (a * psi_powers) % q
    b_twisted = (b * psi_powers) % q

    # Step 2: forward NTT with psi^2
    A = ntt(a_twisted, q, psi2)
    B = ntt(b_twisted, q, psi2)

    # Step 3: point-wise multiply
    C = (A * B) % q

    # Step 4: inverse NTT
    c_twisted = intt(C, q, psi2)

    # Step 5: untwist
    c = (c_twisted * psi_inv_powers) % q
    return c


# ===================================================================
# Tests
# ===================================================================

if __name__ == "__main__":
    print("=== Ex02: Polynomial Ring R_q = Z_q[X]/(X^N+1) ===\n")

    N = 4
    q = 17

    # --- poly_mod ---
    # X^4 = -1, so [0,0,0,0,1] (= X^4) should reduce to [-1] = [q-1, 0, 0, 0]
    check("poly_mod X^4 -> -1",
          list(poly_mod([0, 0, 0, 0, 1], N, q)), [q - 1, 0, 0, 0])
    # X^5 = -X  -> [0, q-1, 0, 0]
    check("poly_mod X^5 -> -X",
          list(poly_mod([0, 0, 0, 0, 0, 1], N, q)), [0, q - 1, 0, 0])

    # --- poly_add ---
    a = np.array([1, 2, 3, 4], dtype=np.int64)
    b = np.array([5, 6, 7, 8], dtype=np.int64)
    check("poly_add [1,2,3,4]+[5,6,7,8] mod 17",
          list(poly_add(a, b, N, q)), [6, 8, 10, 12])

    a2 = np.array([10, 15, 16, 1], dtype=np.int64)
    b2 = np.array([8, 3, 2, 16], dtype=np.int64)
    check("poly_add with wrap",
          list(poly_add(a2, b2, N, q)), [1, 1, 1, 0])

    # --- poly_mul_schoolbook ---
    # (1 + X) * (1 + X) = 1 + 2X + X^2  in R_q (degree < N, no wrap)
    p1 = np.array([1, 1, 0, 0], dtype=np.int64)
    check("schoolbook (1+X)^2",
          list(poly_mul_schoolbook(p1, p1, N, q)), [1, 2, 1, 0])

    # (1 + X^3) * (1 + X^3) = 1 + 2X^3 + X^6
    #   X^6 = X^4 * X^2 = -X^2, so result = 1 + (-1)*X^2 + 2*X^3 = [1, 0, 16, 2]
    p2 = np.array([1, 0, 0, 1], dtype=np.int64)
    check("schoolbook (1+X^3)^2 with negacyclic wrap",
          list(poly_mul_schoolbook(p2, p2, N, q)), [1, 0, q - 1, 2])

    # --- poly_mul_ntt ---
    psi = 2  # primitive 8th root of unity mod 17
    check("NTT mul matches schoolbook for (1+X)^2",
          list(poly_mul_ntt(p1, p1, N, q, psi)),
          list(poly_mul_schoolbook(p1, p1, N, q)))

    check("NTT mul matches schoolbook for (1+X^3)^2",
          list(poly_mul_ntt(p2, p2, N, q, psi)),
          list(poly_mul_schoolbook(p2, p2, N, q)))

    # Random test
    np.random.seed(42)
    ra = np.random.randint(0, q, N)
    rb = np.random.randint(0, q, N)
    check("NTT mul matches schoolbook (random)",
          list(poly_mul_ntt(ra, rb, N, q, psi)),
          list(poly_mul_schoolbook(ra, rb, N, q)))

    summary()
