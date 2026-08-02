/*
 * Exercise 11: Galois Keys, Slot Rotations, Packed MatVec
 * ========================================================
 *
 * WHAT YOU LEARN:
 *   CKKS packs up to N/2 values into "slots" of one ciphertext. Homomorphic
 *   addition and multiplication act slot-wise (SIMD). But cross-slot operations
 *   -- summing all elements, dot products, matrix-vector multiply -- require
 *   ROTATIONS: cyclically shifting slots left or right.
 *
 *   Each rotation offset needs a corresponding Galois key. Forget to generate
 *   the key for an offset you use -> runtime crash. This is the #1 "it compiles
 *   but fails at runtime" bug in CKKS code.
 *
 * WHAT YOU DO:
 *   1. Set up a CKKS context with rotation support
 *   2. Generate Galois keys for specific rotation offsets
 *   3. Encrypt a vector, rotate by different amounts, inspect results
 *   4. Implement sum_all_slots via log-reduction (rotate-and-add)
 *   5. Implement a diagonal matrix-vector product using rotations
 *
 * THEORY REMINDER (from theory.md section 7):
 *   Rotations use the key-switching machinery. Each rotation index requires
 *   a Galois key that the evaluator stores. Generating keys for ALL possible
 *   offsets is expensive (memory); in practice, generate only the ones your
 *   circuit needs.
 *
 * BUILD:
 *   mkdir build && cd build && cmake .. && make ex11_rotations
 *   ./ex11_rotations
 */

#include "openfhe.h"                    // [VERIFY] main OpenFHE header
using namespace lbcrypto;               // [VERIFY] OpenFHE namespace

int main() {
    std::cout << "=== Exercise 11: Rotations, Slot Summation, Packed MatVec ===" << std::endl;
    std::cout << std::endl;

    // -----------------------------------------------------------------------
    // Step 1: Set up CKKS context
    // -----------------------------------------------------------------------
    CCParams<CryptoContextCKKSRNS> parameters;         // [VERIFY]
    parameters.SetMultiplicativeDepth(2);               // [VERIFY] enough for one mult in matvec
    parameters.SetScalingModSize(50);                   // [VERIFY]
    parameters.SetBatchSize(8);                         // [VERIFY] 8 slots for readability
    parameters.SetScalingTechnique(FIXEDAUTO);          // [VERIFY] auto rescale/relin for simplicity
    // Using FIXEDAUTO here so we can focus on rotations, not rescale/relin.

    auto cc = GenCryptoContext(parameters);             // [VERIFY]
    cc->Enable(PKE);                                    // [VERIFY]
    cc->Enable(KEYSWITCH);                              // [VERIFY]
    cc->Enable(LEVELEDSHE);                             // [VERIFY]

    std::cout << "[Setup] CKKS context created (FIXEDAUTO scaling)." << std::endl;
    std::cout << "  Ring dimension N: " << cc->GetRingDimension() << std::endl;  // [VERIFY]
    std::cout << "  Usable slots:     " << cc->GetRingDimension() / 2 << std::endl;
    std::cout << std::endl;

    // -----------------------------------------------------------------------
    // Step 2: Key generation with Galois (rotation) keys
    // -----------------------------------------------------------------------
    auto keys = cc->KeyGen();                           // [VERIFY]
    cc->EvalMultKeyGen(keys.secretKey);                 // [VERIFY] relin key (needed for matvec)

    // === YOUR TASK ===
    // Generate rotation keys for these offsets: {-1, -2, -4, 1, 2, 4}
    // Positive = rotate left (standard convention in OpenFHE).
    // Negative = rotate right.
    // You MUST generate a key for every rotation offset your circuit uses.

    std::vector<int32_t> rotation_indices = {-1, -2, -4, 1, 2, 4};
    cc->EvalRotateKeyGen(keys.secretKey, rotation_indices);  // [VERIFY] method name and signature

    std::cout << "[KeyGen] Keys generated. Rotation keys for indices: ";
    for (auto idx : rotation_indices) std::cout << idx << " ";
    std::cout << std::endl << std::endl;

    // -----------------------------------------------------------------------
    // Step 3: Encrypt a vector and demonstrate rotations
    // -----------------------------------------------------------------------
    std::vector<double> vec = {1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0};
    auto pt = cc->MakeCKKSPackedPlaintext(vec);         // [VERIFY]
    auto ct = cc->Encrypt(keys.publicKey, pt);          // [VERIFY]

    std::cout << "[Rotations] Original vector:  [1, 2, 3, 4, 5, 6, 7, 8]" << std::endl;
    std::cout << std::endl;

    // Rotate by different offsets and decrypt to see the effect
    std::vector<int> offsets_to_try = {1, 2, 4, -1};
    for (int offset : offsets_to_try) {
        auto ct_rotated = cc->EvalRotate(ct, offset);   // [VERIFY] EvalRotate signature
        Plaintext pt_rotated;
        cc->Decrypt(keys.secretKey, ct_rotated, &pt_rotated);  // [VERIFY]
        pt_rotated->SetLength(8);                        // [VERIFY]
        auto vals = pt_rotated->GetRealPackedValue();    // [VERIFY]

        std::cout << "  Rotate by " << std::setw(2) << offset << ": [";
        for (size_t i = 0; i < vals.size(); i++) {
            if (i > 0) std::cout << ", ";
            std::cout << std::fixed << std::setprecision(1) << vals[i];
        }
        std::cout << "]" << std::endl;
    }
    // Expected: rotate left by 1 -> [2, 3, 4, 5, 6, 7, 8, 0(ish)]
    // (Trailing slots wrap cyclically; may show near-zero values from empty slots)
    std::cout << std::endl;

    // -----------------------------------------------------------------------
    // Step 4: Sum all slots via log-reduction
    // -----------------------------------------------------------------------
    // === YOUR TASK ===
    // Implement sum_all_slots: for 8 slots, we need log2(8)=3 rotate-and-add steps.
    //   Step 1: rotate by 4, add -> pairs summed across halves
    //   Step 2: rotate by 2, add -> groups of 4 summed
    //   Step 3: rotate by 1, add -> all 8 summed (result replicated in all slots)
    //
    // This is the fundamental building block for dot products in CKKS.

    std::cout << "[Sum All Slots] Log-reduce summing 8 slots:" << std::endl;

    auto ct_sum = ct;  // start with the original ciphertext
    int num_slots = 8;
    // Log-reduce: rotate by N/2, N/4, ..., 1 and add
    for (int step = num_slots / 2; step >= 1; step /= 2) {
        auto ct_rotated = cc->EvalRotate(ct_sum, step);  // [VERIFY]
        ct_sum = cc->EvalAdd(ct_sum, ct_rotated);         // [VERIFY] EvalAdd signature
        std::cout << "  After rotate-by-" << step << " + add: ";

        // Decrypt intermediate to show progress (expensive; only for learning!)
        Plaintext pt_inter;
        cc->Decrypt(keys.secretKey, ct_sum, &pt_inter);   // [VERIFY]
        pt_inter->SetLength(8);                           // [VERIFY]
        auto inter_vals = pt_inter->GetRealPackedValue(); // [VERIFY]
        std::cout << "[";
        for (size_t i = 0; i < inter_vals.size(); i++) {
            if (i > 0) std::cout << ", ";
            std::cout << std::fixed << std::setprecision(1) << inter_vals[i];
        }
        std::cout << "]" << std::endl;
    }

    // Verify: sum of 1+2+3+4+5+6+7+8 = 36
    Plaintext pt_sum_final;
    cc->Decrypt(keys.secretKey, ct_sum, &pt_sum_final);   // [VERIFY]
    pt_sum_final->SetLength(1);                           // [VERIFY]
    auto sum_val = pt_sum_final->GetRealPackedValue()[0];  // [VERIFY]
    std::cout << "  Final sum (slot 0): " << sum_val << "  (expected: 36)" << std::endl;
    if (std::abs(sum_val - 36.0) < 0.1) {
        std::cout << "  [PASS] Slot summation correct." << std::endl;
    } else {
        std::cout << "  [FAIL] Sum mismatch." << std::endl;
    }
    std::cout << std::endl;

    // -----------------------------------------------------------------------
    // Step 5: Diagonal matrix-vector product
    // -----------------------------------------------------------------------
    // === YOUR TASK ===
    // A common CKKS pattern for matrix-vector multiplication uses the
    // "diagonal method" (Halevi-Shoup). For an n x n matrix M and vector v:
    //
    //   result = sum over k of: diag_k(M) * rotate(v, k)
    //
    // where diag_k extracts the k-th diagonal of M (wrapping cyclically).
    //
    // Example 4x4 matrix (we use first 4 slots of our 8-slot ciphertexts):
    //   M = [[1, 2, 3, 4],     diag_0 = [1, 6, 11, 16]
    //        [5, 6, 7, 8],     diag_1 = [2, 7, 12, 13]
    //        [9, 10, 11, 12],  diag_2 = [3, 8, 9, 14]
    //        [13, 14, 15, 16]] diag_3 = [4, 5, 10, 15]
    //
    // diag_k(i) = M[i][(i+k) % n]

    std::cout << "[Diagonal MatVec] 4x4 matrix-vector product using rotations:" << std::endl;

    int n = 4;
    // The matrix M (row-major)
    double M[4][4] = {
        {1,  2,  3,  4},
        {5,  6,  7,  8},
        {9,  10, 11, 12},
        {13, 14, 15, 16}
    };

    // The input vector
    std::vector<double> v = {1.0, 2.0, 3.0, 4.0, 0.0, 0.0, 0.0, 0.0};

    auto pt_v = cc->MakeCKKSPackedPlaintext(v);          // [VERIFY]
    auto ct_v = cc->Encrypt(keys.publicKey, pt_v);       // [VERIFY]

    // Extract diagonals and compute: result = sum_k( diag_k * rotate(ct_v, k) )
    Ciphertext<DCRTPoly> ct_matvec;                      // [VERIFY] Ciphertext template type

    for (int k = 0; k < n; k++) {
        // Extract diagonal k: diag_k[i] = M[i][(i+k) % n]
        std::vector<double> diag(8, 0.0);
        for (int i = 0; i < n; i++) {
            diag[i] = M[i][(i + k) % n];
        }

        std::cout << "  diag_" << k << " = [";
        for (int i = 0; i < n; i++) {
            if (i > 0) std::cout << ", ";
            std::cout << diag[i];
        }
        std::cout << "]" << std::endl;

        // Encode the diagonal as a plaintext
        auto pt_diag = cc->MakeCKKSPackedPlaintext(diag);  // [VERIFY]

        // Rotate the input vector by k positions
        Ciphertext<DCRTPoly> ct_v_rotated;               // [VERIFY]
        if (k == 0) {
            ct_v_rotated = ct_v;
        } else {
            ct_v_rotated = cc->EvalRotate(ct_v, k);      // [VERIFY]
        }

        // Multiply: diag_k * rotate(v, k)  (plaintext-ciphertext multiply)
        auto ct_term = cc->EvalMult(ct_v_rotated, pt_diag);  // [VERIFY] EvalMult(ct, pt) overload

        // Accumulate
        if (k == 0) {
            ct_matvec = ct_term;
        } else {
            ct_matvec = cc->EvalAdd(ct_matvec, ct_term);  // [VERIFY]
        }
    }

    // Decrypt and verify
    Plaintext pt_matvec;
    cc->Decrypt(keys.secretKey, ct_matvec, &pt_matvec);    // [VERIFY]
    pt_matvec->SetLength(n);                               // [VERIFY]
    auto matvec_result = pt_matvec->GetRealPackedValue();  // [VERIFY]

    // Compute expected result in plaintext
    std::cout << std::endl;
    std::cout << "  Decrypted vs Expected (M * v):" << std::endl;
    double max_error = 0.0;
    for (int i = 0; i < n; i++) {
        double expected = 0;
        for (int j = 0; j < n; j++) {
            expected += M[i][j] * v[j];
        }
        double error = std::abs(expected - matvec_result[i]);
        max_error = std::max(max_error, error);
        std::cout << "    row " << i << ": expected = " << expected
                  << ", got = " << std::fixed << std::setprecision(4) << matvec_result[i]
                  << ", error = " << error << std::endl;
    }
    // Expected: M * [1,2,3,4] = [30, 70, 110, 150]

    std::cout << std::endl;
    std::cout << "  Max error: " << max_error << std::endl;
    if (max_error < 0.1) {
        std::cout << "  [PASS] Matrix-vector product correct." << std::endl;
    } else {
        std::cout << "  [FAIL] Matrix-vector product error too large." << std::endl;
    }

    // -----------------------------------------------------------------------
    // Summary
    // -----------------------------------------------------------------------
    std::cout << std::endl;
    std::cout << "=== Key Takeaways ===" << std::endl;
    std::cout << "  1. Every rotation offset needs a Galois key (EvalRotateKeyGen)." << std::endl;
    std::cout << "  2. Slot summation = log(n) rotate-and-add steps." << std::endl;
    std::cout << "  3. Matrix-vector multiply uses the diagonal method:" << std::endl;
    std::cout << "     result = sum_k( diag_k(M) * rotate(v, k) )" << std::endl;
    std::cout << "  4. This pattern is the foundation of encrypted linear layers in CKKS ML." << std::endl;

    return 0;
}
