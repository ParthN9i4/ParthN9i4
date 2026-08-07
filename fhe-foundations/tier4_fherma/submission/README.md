# FHERMA submission harness

A ready-to-fill OpenFHE C++ submission matching the real FHERMA contract, plus
the depth arithmetic that decides whether it runs.

## The contract

The evaluator builds your project and invokes the binary with six paths to
OpenFHE **binary-serialized** objects:

```
./solution --cc cc.bin --key_pub pub.bin --key_mult mult.bin \
           --key_rot rot.bin --input in.bin --output out.bin
```

You get a CryptoContext, a public key, an evaluation (relinearization) key, a
rotation key, and one input ciphertext. **There is no secret key.** Nothing in
your solution may depend on seeing a plaintext value — no decrypting an
intermediate, no branching on a comparison result. If your approach needs
either, it needs redesigning, not debugging.

| File | Yours to edit? | Purpose |
|---|---|---|
| `main.cpp` | No | Argument parsing; matches the official template |
| `yourSolution.h` | No | Class shape the evaluator depends on |
| `yourSolution.cpp` | **Yes — `eval()` only** | Your homomorphic computation |
| `config.json` | **Yes** | Parameters you declare to the evaluator |
| `CMakeLists.txt` | Rarely | Build definition |

## Declaring parameters correctly

`config.json` is where most submissions fail, because two of its fields are
easy to get wrong in ways that only surface inside the evaluator.

**`mult_depth` — compute it, don't guess it.** Use `../fherma_config.py`:

```bash
python3 ../fherma_config.py          # worked budget + self-tests
```

```python
from fherma_config import circuit_depth, build_config
depth = circuit_depth(ct_mults=1, pt_mults=2, chebyshev_degrees=[7])
cfg   = build_config(mult_depth=depth, rotation_indices=[1, 2, 4, 8])
```

Two traps it encodes, both verified against OpenFHE rather than assumed:

- `EvalChebyshevFunction` costs **more** than `ceil(log2(degree+1))`. A
  degree-15 fit costs **6** levels, not 4. The authoritative mapping is
  OpenFHE's `src/pke/examples/FUNCTION_EVALUATION.md`.
- **Plaintext multiplies cost a level.** Multiplying by a plaintext multiplies
  the scale and forces a rescale. Only additions are free. Counting only
  ciphertext×ciphertext multiplies routinely understates depth by 2–3.

**`indexes_for_rotation_key` — list every offset you use.** OpenFHE throws at
the `EvalRotate` call for any offset without a generated key. A log-reduce sum
over 8 slots uses `{1,2,4}`; a Halevi–Shoup diagonal matvec over an `n×n`
matrix uses `{1..n-1}`, which includes non-powers-of-two. Validate before
submitting:

```python
from fherma_config import validate_config
problems = validate_config(cfg, rotations_used=[1, 2, 3], declared_depth_needed=depth)
```

**Ring dimension follows from depth.** `smallest_ring()` picks it, checking
`logQP` — the chain *plus* the auxiliary modulus HYBRID key switching needs —
against the 128-bit security caps. Forgetting that auxiliary modulus is how you
predict N=8192 and get handed 16384.

## The optimisation loop

FHERMA scores accuracy **and** cost, so the work is: meet the accuracy bar at
the lowest degree possible, because degree drives depth, depth drives ring
dimension, and ring dimension drives runtime.

1. Fit the challenge's target function; find the lowest degree meeting its
   error bound (`../ex18_activation_challenge.py` automates this search).
2. Compute the depth that degree implies, and generate `config.json`.
3. Implement `eval()`; keep the critical path as shallow as the fit allows.
4. Validate locally, then submit.

Chebyshev/minimax fits beat Taylor expansions decisively here — a Taylor series
optimises accuracy at a single point, while these spread error across the whole
interval. See `../ex14_poly_activation.py`.

## Local validation

- **White-box challenges** — validate locally with the
  [`yashalabinc/fherma-validator`](https://hub.docker.com/r/yashalabinc/fherma-validator)
  Docker image before submitting.
- **Black-box challenges** — test cases are on the challenge's Play tab; check
  the results yourself. The primary metric is usually accuracy.

Which type a challenge is, and its exact I/O, are stated on its page:
[fherma.io/challenges](https://fherma.io/challenges) ·
[participation guide](https://fherma.io/how_it_works) ·
[templates and examples](https://github.com/fairmath/fherma-challenges) ·
[polycircuit component library](https://github.com/fairmath/polycircuit)

Other supported stacks: OpenFHE-Python, OpenFHE-rs, and Apple's
swift-homomorphic-encryption. This harness targets the C++ path.

## Pre-submission checklist

- [ ] `eval()` never calls `.decrypt()` or otherwise assumes a secret key
- [ ] `mult_depth` computed from OpenFHE's table, counting plaintext multiplies
- [ ] every rotation offset used appears in `indexes_for_rotation_key`
- [ ] `validate_config(...)` returns no problems
- [ ] builds clean from a fresh `build/` directory
- [ ] runs end-to-end on the challenge's sample artifacts
- [ ] degree is the *lowest* that meets the accuracy bar, not the first that worked
