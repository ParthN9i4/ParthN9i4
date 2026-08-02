# Tier 4 -- FHERMA Preparation

## What is FHERMA?

FHERMA (https://fherma.io) is Fair Math's competitive benchmarking platform
for Fully Homomorphic Encryption.  It hosts challenges where participants
implement FHE computations that are evaluated on accuracy, performance, and
correctness against standardized test suites.

Think of it as "Kaggle for FHE" -- you submit code that operates on
encrypted data, and the platform measures how well your solution works.

## Getting Started

1. **Register** at https://fherma.io (free account).
2. **Browse challenges** -- each has a description, input/output format,
   evaluation criteria, and a leaderboard.
3. **Clone the challenge templates:**
   ```
   git clone https://github.com/fairmath/fherma-challenges
   ```
4. **Study past solutions** to understand what works.

## Challenge Structure

A typical FHERMA challenge provides:

- **Scheme specification**: which FHE scheme to use (BFV, BGV, CKKS, TFHE).
- **Security level**: minimum security parameter (e.g., 128-bit).
- **Input format**: serialized OpenFHE ciphertexts, crypto context, and
  keys (public key, evaluation keys).
- **Evaluation function**: the function you must implement. It receives
  encrypted inputs and must produce encrypted outputs.
- **Accuracy metric**: maximum allowed error (for CKKS) or exact match
  (for BFV/BGV).
- **Performance metric**: execution time, multiplicative depth, or
  circuit size.

### Common Challenge Types

| Type | Description | Key Skill |
|------|-------------|-----------|
| Polynomial activation | Approximate a non-linear function (sigmoid, ReLU, GELU) with a polynomial under depth/error constraints | Chebyshev/Remez approximation (ex14, ex18) |
| Encrypted comparison | Implement < or > on encrypted integers | Bit decomposition, Boolean circuits |
| Matrix operations | Encrypted matrix multiply, transpose, or inversion | Slot packing, rotation optimization |
| Statistical functions | Mean, variance, sorting on encrypted data | Combining comparison + arithmetic |
| Machine learning | Encrypted inference (logistic regression, neural nets) | Everything from tier 3 |

## How Tier 0-3 Maps to FHERMA

| Exercise | FHERMA Competency |
|----------|-------------------|
| ex01-02 (modular arithmetic, rings) | Understanding the algebraic foundation of all FHE schemes |
| ex06-08 (CKKS basics) | Working with ciphertexts, understanding noise and depth |
| ex09-12 (engineering) | Managing depth budgets, choosing parameters, debugging |
| ex13 (logistic regression) | Encrypted ML inference challenges |
| ex14 (Chebyshev approximation) | **Directly applicable** to polynomial activation challenges |
| ex15 (Concrete-ML XGBoost) | Understanding quantization trade-offs |
| ex16 (encrypted NN) | End-to-end encrypted inference pipeline |
| ex17 (challenge template) | Understanding FHERMA submission structure |
| ex18 (activation optimization) | The exact workflow for activation function challenges |

## Tips for Activation Function Challenges

These are where your Chebyshev/Remez skills from ex14 apply directly:

1. **Start with Chebyshev interpolation** at a moderate degree (7-11).
   Measure the max error.
2. **Increase degree** until you meet the accuracy threshold, but no further
   -- every extra degree costs multiplicative depth.
3. **Consider the domain carefully.** Many challenges specify the input range.
   A narrower range needs fewer terms for the same accuracy.
4. **Exploit symmetry.** Sigmoid is antisymmetric around 0 (after shifting by
   0.5), so only odd Chebyshev terms are nonzero -- you can skip even terms
   and halve your depth.
5. **Remez algorithm** gives the true minimax polynomial, which is optimal.
   Chebyshev is near-optimal and much easier to compute -- start there, then
   try Remez if you need to shave off one more degree.
6. **Test on the exact evaluation grid** the challenge uses, not just random
   points. Edge cases near domain boundaries often have the highest error.

## Running the Exercises

```bash
# From the fhe-foundations directory:
python tier4_fherma/ex17_fherma_template.py
python tier4_fherma/ex18_activation_challenge.py
```

Both exercises are pure Python (no FHE library required) and focus on the
algorithmic and optimization skills needed for FHERMA submissions.
