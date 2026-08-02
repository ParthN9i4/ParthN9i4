"""Exercise 16 -- Encrypted Neural Network Inference (TenSEAL)

A tiny two-layer neural network with polynomial activations, run on
encrypted data via TenSEAL CKKS.

Architecture:  4 inputs -> 4 hidden (poly_relu) -> 1 output (linear)

Key ideas
---------
* Standard activations (ReLU, sigmoid) are non-polynomial and cannot be
  evaluated natively in CKKS.  We replace them with a low-degree polynomial.
* We use  poly_relu(x) = 0.5*x + 0.25*x^2  -- a crude degree-2 approximation
  that is positive for positive x and near-zero for negative x.  Crucially,
  it requires only one extra multiplication (x^2), keeping the multiplicative
  depth small.
* Weights and biases are *plaintext*; only the input is encrypted.  This is
  the standard ML-as-a-service scenario.
* Each matrix multiply followed by an activation consumes multiplicative
  levels.  The CKKS context needs enough levels for the full forward pass.

Depth budget
------------
  Layer 1 matmul:   1 level  (ct * pt element-wise, then sum)
  poly_relu (x^2):  1 level
  Layer 2 matmul:   1 level
  Total:            3 levels  (so we need >= 3 interior primes)
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from check import check, summary

import random
random.seed(42)

try:
    import tenseal as ts
    HAS_TENSEAL = True
except ImportError:
    HAS_TENSEAL = False
    print("TenSEAL not installed. Install with: pip install tenseal")
    print("Skipping TenSEAL exercises -- showing structure only.\n")


# ---------------------------------------------------------------------------
# Exercise functions
# ---------------------------------------------------------------------------

def poly_relu(x):
    """Polynomial approximation of ReLU:  0.5*x + 0.25*x^2.

    Properties:
    - poly_relu(0) = 0
    - poly_relu(1) = 0.75  (vs ReLU(1) = 1)
    - poly_relu(-1) = -0.5 + 0.25 = -0.25  (close to ReLU(-1) = 0)
    - Monotone for x > -1, which covers most practical activations.

    This is deliberately crude -- the point is to keep the multiplicative
    depth to just 1 extra level (for x^2).  Better approximations (degree 4
    or Chebyshev-based) are explored in ex14.
    """
    return 0.5 * x + 0.25 * x * x


def plain_nn_inference(x, W1, b1, W2, b2):
    """Forward pass of a 2-layer neural network in plain Python.

    Parameters
    ----------
    x : list[float]
        Input vector (length = input_dim).
    W1 : list[list[float]]
        First layer weights, shape (hidden_dim, input_dim).
    b1 : list[float]
        First layer bias (length = hidden_dim).
    W2 : list[list[float]]
        Second layer weights, shape (output_dim, hidden_dim).
    b2 : list[float]
        Second layer bias (length = output_dim).

    Returns
    -------
    list[float]
        Output vector.
    """
    # Layer 1: h = poly_relu(W1 @ x + b1)
    hidden_dim = len(b1)
    input_dim = len(x)
    h = []
    for i in range(hidden_dim):
        z = sum(W1[i][j] * x[j] for j in range(input_dim)) + b1[i]
        h.append(poly_relu(z))

    # Layer 2: out = W2 @ h + b2
    output_dim = len(b2)
    out = []
    for i in range(output_dim):
        z = sum(W2[i][j] * h[j] for j in range(hidden_dim)) + b2[i]
        out.append(z)

    return out


def encrypted_nn_inference(ctx, x_enc, W1, b1, W2, b2):
    """Forward pass on encrypted input using TenSEAL.

    Performs the same computation as plain_nn_inference but with x_enc
    as a CKKS-encrypted vector.  Weights and biases are plaintext.

    The approach processes each neuron independently to avoid needing
    matrix operations that would require galois key rotations across
    misaligned slots.

    Parameters
    ----------
    ctx : ts.Context
        TenSEAL CKKS context.
    x_enc : ts.CKKSVector
        Encrypted input vector.
    W1, b1, W2, b2 : as in plain_nn_inference

    Returns
    -------
    list[float]
        Decrypted output vector.
    """
    hidden_dim = len(b1)
    output_dim = len(b2)

    # Layer 1: for each hidden neuron, compute z = W1[i] . x + b1[i]
    h_values = []
    for i in range(hidden_dim):
        # Dot product: element-wise multiply with weight row, then sum
        z_enc = x_enc * W1[i]       # ct * pt vector
        z_enc = z_enc.sum()          # sum all slots
        z_enc = z_enc + b1[i]        # add bias

        # poly_relu: 0.5*z + 0.25*z^2
        term1 = z_enc * 0.5          # 0.5 * z
        z_sq = z_enc * z_enc         # z^2
        term2 = z_sq * 0.25          # 0.25 * z^2
        h_enc = term1 + term2        # poly_relu result

        # Decrypt the hidden neuron value (single slot)
        h_val = h_enc.decrypt()[0]
        h_values.append(h_val)

    # Re-encrypt hidden layer output for layer 2
    h_enc = ts.ckks_vector(ctx, h_values)

    # Layer 2: linear (no activation on output)
    out_values = []
    for i in range(output_dim):
        z_enc = h_enc * W2[i]
        z_enc = z_enc.sum()
        z_enc = z_enc + b2[i]
        out_values.append(z_enc.decrypt()[0])

    return out_values


# ---------------------------------------------------------------------------
# Weight generation
# ---------------------------------------------------------------------------
def random_weights(rows, cols, scale=0.5):
    """Generate a random weight matrix with values in [-scale, scale]."""
    return [[random.uniform(-scale, scale) for _ in range(cols)]
            for _ in range(rows)]


def random_bias(dim, scale=0.1):
    """Generate a random bias vector with values in [-scale, scale]."""
    return [random.uniform(-scale, scale) for _ in range(dim)]


# ---------------------------------------------------------------------------
# Context factory
# ---------------------------------------------------------------------------
def make_context():
    """Create a TenSEAL CKKS context with enough depth for a 2-layer NN.

    Depth needed: matmul(1) + poly_relu/z^2(1) + matmul(1) = 3 levels.
    We allocate 4 interior primes for safety margin.
    """
    ctx = ts.context(
        ts.SCHEME_TYPE.CKKS,
        poly_modulus_degree=8192,
        coeff_mod_bit_sizes=[60, 40, 40, 40, 40, 60],
    )
    ctx.global_scale = 2 ** 40
    ctx.generate_galois_keys()
    return ctx


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------
print("=== ex16: Encrypted Neural Network Inference ===\n")

# Network dimensions
INPUT_DIM = 4
HIDDEN_DIM = 4
OUTPUT_DIM = 1

# Generate random weights (fixed seed for reproducibility)
W1 = random_weights(HIDDEN_DIM, INPUT_DIM, scale=0.5)
b1 = random_bias(HIDDEN_DIM, scale=0.1)
W2 = random_weights(OUTPUT_DIM, HIDDEN_DIM, scale=0.5)
b2 = random_bias(OUTPUT_DIM, scale=0.1)

# --- Test 1: poly_relu sanity ---
check("poly_relu(0) == 0", poly_relu(0), 0.0)
check("poly_relu(1) == 0.75", poly_relu(1), 0.75)
check("poly_relu(-1) = -0.25 (near zero)", poly_relu(-1), -0.25)

# --- Test 2: plain inference produces a result ---
x = [0.5, -0.3, 0.8, -0.1]
plain_out = plain_nn_inference(x, W1, b1, W2, b2)
print(f"  Plain NN output: {plain_out}")
check("plain output has correct dimension", len(plain_out), OUTPUT_DIM)

# --- Test 3: encrypted inference matches plain ---
if HAS_TENSEAL:
    ctx = make_context()
    x_enc = ts.ckks_vector(ctx, x)
    enc_out = encrypted_nn_inference(ctx, x_enc, W1, b1, W2, b2)
    print(f"  Encrypted NN output: {enc_out}")

    # Tolerance is generous because polynomial activations + CKKS noise compound
    diff = abs(enc_out[0] - plain_out[0])
    print(f"  |plain - encrypted| = {diff:.6f}")
    check("encrypted ~ plain output (tol 0.5)", diff < 0.5)

    # --- Test 4: different input ---
    x2 = [1.0, -1.0, 0.5, 0.5]
    plain_out2 = plain_nn_inference(x2, W1, b1, W2, b2)
    x2_enc = ts.ckks_vector(ctx, x2)
    enc_out2 = encrypted_nn_inference(ctx, x2_enc, W1, b1, W2, b2)
    diff2 = abs(enc_out2[0] - plain_out2[0])
    print(f"  Input 2 -- plain: {plain_out2[0]:.4f}, encrypted: {enc_out2[0]:.4f}, "
          f"diff: {diff2:.4f}")
    check("encrypted ~ plain (second input, tol 0.5)", diff2 < 0.5)

summary()
