# FHE Foundations — Coding Exercise Ladder

A hands-on exercise sequence that builds from raw modular arithmetic up to encrypted ML
inference and FHERMA challenge preparation. Companion to the FHE book (`fhe-book.html`).

## How to use

Each exercise is a standalone file. Run it directly:

```bash
python3 tier0_math/ex01_modular_arith.py
```

Every file contains:
- A short docstring explaining the concept (the book has the full treatment)
- Reference implementations that make all tests pass
- `check()` assertions at the bottom — read these first, they ARE the specification
- Several exercises include a "break it" section where wrong parameters show failure modes

**To learn**: delete a function body (replace with `pass`), re-read the docstring and tests,
then reimplement. The tests tell you when you've got it right.

## Tier progression

| Tier | Directory | Dependencies | What you learn |
|------|-----------|-------------|----------------|
| 0 | `tier0_math/` | numpy, scipy | Build LWE, RLWE, NTT, CKKS encoding from scratch |
| 1 | `tier1_ckks/` | tenseal | First real encrypted computation (CKKS, auto rescale) |
| 2 | `tier2_engineering/` | OpenFHE (C++) | Manual rescale, relin, rotations, depth budgeting |
| 3 | `tier3_ml/` | tenseal, concrete-ml | Encrypted inference, polynomial activations, FHE trees |
| 4 | `tier4_fherma/` | numpy | FHERMA challenge structure, activation optimization |

## Installation

```bash
# Tier 0 — pure math
pip install numpy scipy

# Tier 1 & 3 — TenSEAL
pip install tenseal

# Tier 2 — OpenFHE (C++, build from source)
git clone https://github.com/openfheorg/openfhe-development.git
cd openfhe-development && mkdir build && cd build
cmake .. && make -j$(nproc) && sudo make install

# Tier 3 — Concrete-ML (optional, for ex15)
pip install concrete-ml

# Tier 4 — FHERMA reference challenges
git clone https://github.com/fairmath/fherma-challenges.git
```

## Exercise index

### Tier 0 — Pure math (numpy only)
- **ex01** Modular arithmetic: Z_q, CRT, NTT
- **ex02** Ring polynomials: R_q = Z_q[X]/(X^N+1), negacyclic convolution
- **ex03** LWE encryption: toy scheme + deliberate noise failure
- **ex04** RLWE encryption: homomorphic add/multiply on ring elements
- **ex05** CKKS encoding: canonical embedding, encode/decode real numbers

### Tier 1 — TenSEAL CKKS
- **ex06** First encrypt: encrypt, add, multiply, decrypt
- **ex07** Dot product: encrypted dot product, measure approximation error
- **ex08** Polynomial evaluation: ax² + bx + c on encrypted data
- **ex09** Depth limit: push past the budget, observe the failure

### Tier 2 — OpenFHE C++ (skeletons, verify against current API)
- **ex10** Manual CKKS: explicit rescale and relinearize
- **ex11** Rotations: Galois keys, slot permutations, packed matmul
- **ex12** Depth budget: parameter selection, ring dimension growth

### Tier 3 — Encrypted ML
- **ex13** Logistic regression on encrypted data (TenSEAL)
- **ex14** Polynomial activation approximation — Chebyshev/Remez (numpy)
- **ex15** Encrypted XGBoost (Concrete-ML)
- **ex16** Encrypted neural network inference (TenSEAL)

### Tier 4 — FHERMA preparation
- **ex17** FHERMA challenge template: understand the submission format
- **ex18** Activation challenge: optimize polynomial degree vs accuracy under depth budget

## Confidence tags

- Code using **numpy** — fully standalone, runs as-is
- Code using **TenSEAL / Concrete-ML** — verified Python API, runs after `pip install`
- Code using **OpenFHE C++** — marked `[VERIFY]` where API signatures should be checked
  against current OpenFHE examples before compiling

## Connection to FHERMA

Your existing strength in Chebyshev/Remez polynomial approximation for activation functions
maps directly to FHERMA's activation-function challenges (ReLU, GELU, softmax, sign).
The tier 4 exercises simulate the optimization loop: given a function to evaluate
homomorphically, minimize depth while maintaining accuracy — exactly the FHERMA scoring metric.
