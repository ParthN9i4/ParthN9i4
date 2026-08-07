"""FHERMA submission config: depth budgeting and config.json generation.

The single most common way to fail a FHERMA submission is not a wrong answer --
it is a circuit that cannot run under the parameters you declared. This module
encodes the arithmetic that decides that, so you can compute `mult_depth`
instead of guessing it.

Two facts drive everything here, both verified against OpenFHE rather than
inferred from the textbook formula:

1. EvalChebyshevFunction costs MORE than ceil(log2(degree+1)) levels. OpenFHE
   ships the authoritative mapping in src/pke/examples/FUNCTION_EVALUATION.md;
   a degree-15 fit costs 6 levels, not the 4 the formula suggests. Budget from
   the table (CHEBYSHEV_DEPTH below), never from the formula.

2. A plaintext multiply costs a level. Multiplying a ciphertext by a plaintext
   multiplies the scale, which forces a rescale, which drops a prime. Only
   additions are free. Counting only ct*ct multiplies is how a circuit runs out
   of levels two thirds of the way through.

Run this file directly to see a worked budget and the self-tests.
"""

import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# --- OpenFHE's degree -> multiplicative depth table -------------------------
# Source: openfhe-development/src/pke/examples/FUNCTION_EVALUATION.md
# Each entry is (max_degree_inclusive, depth) for EvalChebyshevFunction.
CHEBYSHEV_DEPTH = [
    (5, 4), (13, 5), (27, 6), (59, 7), (119, 8), (247, 9),
    (495, 10), (1007, 11), (2031, 12), (4031, 13), (8127, 14),
    (16255, 15), (32639, 16),
]

# SEAL/OpenFHE coefficient-modulus caps at 128-bit classical security, per the
# HomomorphicEncryption.org standard. Used to pick the smallest viable ring.
RING_CAPS = {1024: 27, 2048: 54, 4096: 109, 8192: 218,
             16384: 438, 32768: 881, 65536: 1772, 131072: 3524}


def chebyshev_depth(degree, domain_is_unit=False):
    """Levels consumed by one EvalChebyshevFunction call at this degree.

    Set domain_is_unit=True when evaluating on exactly (-1, 1); OpenFHE
    documents that this case costs one level less.

    Note this is deliberately NOT ceil(log2(degree+1)) -- see module docstring.
    """
    if degree < 3:
        raise ValueError("EvalChebyshevFunction expects degree >= 3")
    for max_deg, depth in CHEBYSHEV_DEPTH:
        if degree <= max_deg:
            return depth - 1 if domain_is_unit else depth
    raise ValueError(f"degree {degree} exceeds the documented table (max 32639)")


def naive_formula_depth(degree):
    """What ceil(log2(degree+1)) predicts -- shown only to contrast with reality."""
    import math
    return math.ceil(math.log2(degree + 1))


def circuit_depth(ct_mults=0, pt_mults=0, chebyshev_degrees=(), domain_is_unit=False):
    """Total multiplicative depth of a circuit.

    Parameters
    ----------
    ct_mults : int
        Ciphertext x ciphertext multiplications along the critical path.
    pt_mults : int
        Ciphertext x plaintext multiplications along the critical path.
        These are NOT free -- each costs one level.
    chebyshev_degrees : iterable of int
        One entry per EvalChebyshevFunction call on the critical path.
    """
    total = ct_mults + pt_mults
    for d in chebyshev_degrees:
        total += chebyshev_depth(d, domain_is_unit)
    return total


def smallest_ring(mult_depth, scale_mod_size=59, first_mod_size=60,
                  key_switch_aux_bits=None):
    """Smallest ring dimension whose 128-bit-security cap fits this chain.

    OpenFHE checks the security table against logQP -- the chain PLUS the
    auxiliary modulus P that HYBRID key switching needs. Forgetting P is the
    standard way to predict one ring dimension and be handed the next one up.
    """
    if key_switch_aux_bits is None:
        key_switch_aux_bits = first_mod_size
    log_q = first_mod_size + mult_depth * scale_mod_size
    log_qp = log_q + key_switch_aux_bits
    for ring, cap in sorted(RING_CAPS.items()):
        if log_qp <= cap:
            return ring, log_q, log_qp
    raise ValueError(f"logQP={log_qp} exceeds every tabulated ring dimension")


def build_config(mult_depth, rotation_indices, scale_mod_size=59,
                 first_mod_size=60, ring_dimension=None, batch_size=None,
                 enable_bootstrapping=False, levels_after_bootstrap=10,
                 level_budget=(4, 4)):
    """Produce a FHERMA config.json dict.

    Field names match templates/openfhe/config.json in
    github.com/fairmath/fherma-challenges. Every rotation offset your circuit
    uses must appear in rotation_indices -- OpenFHE throws at the EvalRotate
    call for any offset without a generated key, and it will not be caught
    until the evaluator runs your binary.
    """
    if ring_dimension is None:
        ring_dimension, _, _ = smallest_ring(mult_depth, scale_mod_size, first_mod_size)
    if batch_size is None:
        batch_size = ring_dimension // 2
    return {
        "indexes_for_rotation_key": sorted(set(int(i) for i in rotation_indices)),
        "mult_depth": int(mult_depth),
        "ring_dimension": int(ring_dimension),
        "scale_mod_size": int(scale_mod_size),
        "first_mod_size": int(first_mod_size),
        "batch_size": int(batch_size),
        "enable_bootstrapping": bool(enable_bootstrapping),
        "levels_available_after_bootstrap": int(levels_after_bootstrap),
        "level_budget": list(level_budget),
    }


def validate_config(cfg, rotations_used=(), declared_depth_needed=None):
    """Check a config for the failure modes that cost submissions.

    Returns a list of human-readable problems; empty means it looks sane.
    """
    problems = []
    required = {"indexes_for_rotation_key", "mult_depth", "ring_dimension",
                "scale_mod_size", "first_mod_size", "batch_size"}
    missing = required - set(cfg)
    if missing:
        problems.append(f"missing required fields: {sorted(missing)}")
        return problems

    declared_rots = set(cfg["indexes_for_rotation_key"])
    ungenerated = set(rotations_used) - declared_rots
    if ungenerated:
        problems.append(
            f"rotation offsets used but not declared: {sorted(ungenerated)} "
            "-- EvalRotate throws at runtime for these")

    if declared_depth_needed is not None and cfg["mult_depth"] < declared_depth_needed:
        problems.append(
            f"mult_depth={cfg['mult_depth']} is below the circuit's requirement "
            f"of {declared_depth_needed}; the chain will be exhausted mid-evaluation")

    log_q = cfg["first_mod_size"] + cfg["mult_depth"] * cfg["scale_mod_size"]
    log_qp = log_q + cfg["first_mod_size"]
    cap = RING_CAPS.get(cfg["ring_dimension"])
    if cap is None:
        problems.append(f"ring_dimension {cfg['ring_dimension']} is not a tabulated power of two")
    elif log_qp > cap:
        problems.append(
            f"logQP~{log_qp} exceeds the {cap}-bit cap for N={cfg['ring_dimension']} "
            "at 128-bit security -- context creation will fail")

    if cfg["batch_size"] > cfg["ring_dimension"] // 2:
        problems.append(
            f"batch_size {cfg['batch_size']} exceeds N/2 = {cfg['ring_dimension']//2} slots")

    return problems


if __name__ == "__main__":
    from check import check, summary

    print("=== FHERMA config: depth budgeting ===\n")

    print("  OpenFHE's real Chebyshev cost vs the textbook formula:")
    print("    degree | OpenFHE table | ceil(log2(d+1)) | understated by")
    print("    -------|---------------|-----------------|---------------")
    for d in (5, 7, 13, 15, 27, 59, 119):
        real, naive = chebyshev_depth(d), naive_formula_depth(d)
        print(f"      {d:4d} |      {real:2d}       |       {naive:2d}        |     {real-naive:+d}")
    print()

    # --- depth table --------------------------------------------------------
    check("degree 5 costs 4 levels", chebyshev_depth(5), 4)
    check("degree 7 costs 5 levels", chebyshev_depth(7), 5)
    check("degree 15 costs 6 levels (not 4)", chebyshev_depth(15), 6)
    check("degree 27 costs 6 levels", chebyshev_depth(27), 6)
    check("degree 28 crosses into 7", chebyshev_depth(28), 7)
    check("unit domain saves one level", chebyshev_depth(15, domain_is_unit=True), 5)
    check("formula understates degree 15", naive_formula_depth(15), 4)

    # --- circuit budgeting --------------------------------------------------
    # Encrypted logistic inference: dot product (pt), domain rescale (pt),
    # degree-7 sigmoid.
    d = circuit_depth(pt_mults=2, chebyshev_degrees=[7])
    check("logistic inference needs 7 levels", d, 7)

    # Forgetting that plaintext multiplies cost levels understates by 2.
    naive = circuit_depth(chebyshev_degrees=[7])
    check("ignoring plaintext mults understates by 2", d - naive, 2)

    # --- ring selection -----------------------------------------------------
    ring, log_q, log_qp = smallest_ring(2, scale_mod_size=50, first_mod_size=60)
    check("depth 2 @ 50-bit primes needs N=16384, not 8192", ring, 16384)
    check("  because logQP exceeds 218", log_qp > 218, True)

    ring1, _, _ = smallest_ring(1, scale_mod_size=50, first_mod_size=60)
    check("depth 1 does fit in 8192", ring1, 8192)

    # --- config generation and validation -----------------------------------
    cfg = build_config(mult_depth=d, rotation_indices=[1, 2, 4, 8])
    check("generated config declares the depth", cfg["mult_depth"], d)
    check("generated config is self-consistent", validate_config(cfg), [])

    # A config that uses an undeclared rotation is the classic runtime failure.
    bad = validate_config(cfg, rotations_used=[1, 2, 3])
    check("undeclared rotation offset is caught", len(bad) == 1 and "3" in bad[0], True)

    # A config whose chain overflows its ring is caught before submission.
    overflow = build_config(mult_depth=10, rotation_indices=[1])
    overflow["ring_dimension"] = 8192
    check("ring overflow is caught", any("exceeds" in p for p in validate_config(overflow)), True)

    print("\n  Example config.json for the logistic-inference circuit:")
    print("  " + json.dumps(cfg, indent=2).replace("\n", "\n  "))

    summary()
