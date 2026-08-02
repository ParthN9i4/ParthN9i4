"""Exercise 09 -- Depth Limits (CKKS)

Every CKKS ciphertext has a finite number of *multiplicative levels*
(determined by the number of primes in coeff_mod_bit_sizes minus one for
each special prime).  Each ciphertext--ciphertext multiplication consumes
one level.  When levels run out, the next multiplication raises an error.

This exercise deliberately uses a *shallow* context -- only 1
multiplicative level -- so you can see the depth wall up close:
  - 1 squaring succeeds  (consumes the single level)
  - 2 squarings fails    (no levels left)

Understanding depth budgets is critical for designing FHE computations.
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
# Shallow context: only 1 multiplicative level
# ---------------------------------------------------------------------------
def make_shallow_context():
    """Create a CKKS context with minimal depth (1 multiplicative level).

    coeff_mod_bit_sizes=[60, 40, 60] gives:
      - 3 primes total
      - 1 special prime (last one, used for key switching)
      - Leaves 2 non-special primes -> 1 multiplicative level
    """
    ctx = ts.context(
        ts.SCHEME_TYPE.CKKS,
        poly_modulus_degree=8192,
        coeff_mod_bit_sizes=[60, 40, 60],
    )
    ctx.global_scale = 2**40
    return ctx


# ---------------------------------------------------------------------------
# Exercise functions
# ---------------------------------------------------------------------------
def successive_squares(ctx, x_vec, n_squarings):
    """Encrypt x_vec and square the ciphertext n_squarings times.

    Returns a list of decrypted results after each successful squaring.
    If a squaring fails (depth exceeded), the list stops at that point
    and the exception message is printed.
    """
    enc = ts.ckks_vector(ctx, x_vec)
    results = []

    for i in range(n_squarings):
        try:
            enc = enc * enc  # squaring = ciphertext * ciphertext
            decrypted = enc.decrypt()
            results.append(decrypted)
        except Exception as e:
            print(f"  INFO  Squaring {i + 1} failed: {type(e).__name__}: {e}")
            break

    return results


def find_depth_limit(ctx, x_vec):
    """Keep squaring until we hit the depth wall.

    Returns the number of *successful* squarings before failure.
    """
    enc = ts.ckks_vector(ctx, x_vec)
    count = 0

    while True:
        try:
            enc = enc * enc
            _ = enc.decrypt()  # force evaluation to detect errors
            count += 1
        except Exception:
            break

    return count


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
if HAS_TENSEAL:
    print("=== ex09: Depth Limits ===\n")

    ctx_shallow = make_shallow_context()
    x_vec = [2.0, 3.0]

    # --- successive_squares: 1 squaring should work ---
    results_1 = successive_squares(ctx_shallow, x_vec, 1)
    check("1 squaring succeeds", len(results_1), 1)
    # After 1 squaring: [2^2, 3^2] = [4, 9]
    if len(results_1) == 1:
        check("squared values correct", results_1[0], [4.0, 9.0], tol=0.1)

    # --- successive_squares: 3 attempts, only 1 should succeed ---
    results_3 = successive_squares(ctx_shallow, x_vec, 3)
    check("only 1 of 3 squarings succeeds", len(results_3), 1)

    # --- find_depth_limit ---
    depth = find_depth_limit(ctx_shallow, x_vec)
    print(f"  INFO  depth limit (successful squarings) = {depth}")
    check("depth limit is 1 for shallow context", depth, 1)

    # --- contrast with deeper context ---
    ctx_deep = ts.context(
        ts.SCHEME_TYPE.CKKS,
        poly_modulus_degree=8192,
        coeff_mod_bit_sizes=[60, 40, 40, 60],
    )
    ctx_deep.global_scale = 2**40
    depth_deep = find_depth_limit(ctx_deep, x_vec)
    print(f"  INFO  depth limit (deeper context)       = {depth_deep}")
    check("deeper context allows more squarings", depth_deep > depth, True)

summary()
