/*
 * Exercise 12: Depth Counting, Parameter Selection, Budget Exhaustion
 * ====================================================================
 *
 * WHAT YOU LEARN:
 *   The multiplicative depth you set in parameters determines EVERYTHING:
 *     - Ring dimension (N): more depth -> larger N -> more memory, slower ops
 *     - Key sizes: grow with N
 *     - Ciphertext sizes: grow with N and the number of moduli in the chain
 *     - Speed: every operation is O(N log N) in the ring dimension
 *
 *   This exercise makes the tradeoff visceral: you will see parameter sizes
 *   at depth 2, 5, and 10, then deliberately exhaust the budget to see the
 *   failure mode.
 *
 * WHAT YOU DO:
 *   1. Create contexts at depth=2, 5, 10 and compare ring dimensions + sizes
 *   2. Perform multiplications up to the depth budget and watch levels drain
 *   3. Exceed the budget and observe the error / garbage output
 *   4. Understand: your circuit's depth dictates your parameter cost
 *
 * KEY INSIGHT:
 *   Designing an FHE circuit is backwards from normal programming.
 *   Normal:  write the algorithm, then deploy.
 *   FHE:     count your multiplications FIRST, then pick parameters that fit.
 *   If your circuit is too deep, you either:
 *     (a) restructure it to reduce depth (e.g., tree-reduce instead of sequential)
 *     (b) accept bigger/slower parameters
 *     (c) use bootstrapping to refresh mid-circuit (expensive but unbounded)
 *
 * BUILD:
 *   mkdir build && cd build && cmake .. && make ex12_depth_budget
 *   ./ex12_depth_budget
 */

#include "openfhe.h"                    // [VERIFY] main OpenFHE header
using namespace lbcrypto;               // [VERIFY] OpenFHE namespace

// Helper: create a CKKS context at a given depth and report its parameters
void report_context_size(int depth) {
    CCParams<CryptoContextCKKSRNS> parameters;         // [VERIFY]
    parameters.SetMultiplicativeDepth(depth);           // [VERIFY]
    parameters.SetScalingModSize(50);                   // [VERIFY]
    parameters.SetBatchSize(8);                         // [VERIFY]
    parameters.SetScalingTechnique(FIXEDAUTO);          // [VERIFY]

    auto cc = GenCryptoContext(parameters);             // [VERIFY]
    cc->Enable(PKE);                                    // [VERIFY]
    cc->Enable(KEYSWITCH);                              // [VERIFY]
    cc->Enable(LEVELEDSHE);                             // [VERIFY]

    uint32_t ring_dim = cc->GetRingDimension();         // [VERIFY] GetRingDimension()

    // The modulus chain has (depth + 1) moduli of ~scalingModSize bits each,
    // plus a special modulus. Total log(Q) ~ (depth+1)*50 + special bits.
    // Ring dimension is chosen to satisfy 128-bit security for that Q.

    // Estimate ciphertext size: each ciphertext is 2 polynomials of N
    // coefficients, stored in RNS with (depth + 1) moduli -- one per level in
    // the chain Q, each ~64 bits. The auxiliary modulus P used by hybrid key
    // switching is NOT counted here: it exists only transiently inside the
    // key-switch operation and is never part of a stored ciphertext.
    // Rough size ~ 2 * N * (depth + 1) * 8 bytes
    size_t est_ct_bytes = 2ULL * ring_dim * (depth + 1) * 8;

    std::cout << "  Depth " << std::setw(2) << depth << ":  "
              << "N = " << std::setw(6) << ring_dim
              << "  |  slots = " << std::setw(5) << ring_dim / 2
              << "  |  est. ciphertext ~ " << std::setw(7) << est_ct_bytes / 1024 << " KB"
              << std::endl;
}

int main() {
    std::cout << "=== Exercise 12: Depth Budget and Parameter Selection ===" << std::endl;
    std::cout << std::endl;

    // -----------------------------------------------------------------------
    // Part 1: Compare parameter sizes at different depths
    // -----------------------------------------------------------------------
    std::cout << "[Part 1] Ring dimension and ciphertext size vs. multiplicative depth:" << std::endl;
    std::cout << "  (128-bit security; scalingModSize = 50 bits)" << std::endl;
    std::cout << std::endl;

    // === YOUR TASK ===
    // Observe how ring dimension jumps (always a power of 2) as depth increases.
    // Think about why: larger Q (more moduli in the chain) requires larger N
    // to maintain 128-bit security against lattice attacks.

    report_context_size(1);
    report_context_size(2);
    report_context_size(3);
    report_context_size(5);
    report_context_size(7);
    report_context_size(10);
    report_context_size(15);
    report_context_size(20);

    std::cout << std::endl;
    std::cout << "  Observation: N doubles when depth roughly doubles." << std::endl;
    std::cout << "  Each doubling of N means ~4x slower multiplications and ~4x more memory." << std::endl;
    std::cout << std::endl;

    // -----------------------------------------------------------------------
    // Part 2: Drain the depth budget with sequential multiplications
    // -----------------------------------------------------------------------
    std::cout << "[Part 2] Watching the level drain: sequential multiplies at depth=5" << std::endl;
    std::cout << std::endl;

    int target_depth = 5;
    CCParams<CryptoContextCKKSRNS> params;             // [VERIFY]
    params.SetMultiplicativeDepth(target_depth);        // [VERIFY]
    params.SetScalingModSize(50);                       // [VERIFY]
    params.SetBatchSize(8);                             // [VERIFY]
    params.SetScalingTechnique(FIXEDAUTO);              // [VERIFY] auto handles rescale/relin

    auto cc = GenCryptoContext(params);                 // [VERIFY]
    cc->Enable(PKE);                                    // [VERIFY]
    cc->Enable(KEYSWITCH);                              // [VERIFY]
    cc->Enable(LEVELEDSHE);                             // [VERIFY]

    auto keys = cc->KeyGen();                           // [VERIFY]
    cc->EvalMultKeyGen(keys.secretKey);                 // [VERIFY]

    // Encrypt a simple vector
    std::vector<double> vec = {2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0, 2.0};
    auto pt = cc->MakeCKKSPackedPlaintext(vec);         // [VERIFY]
    auto ct = cc->Encrypt(keys.publicKey, pt);          // [VERIFY]

    std::cout << "  Start:       level = " << ct->GetLevel()   // [VERIFY]
              << "  (depth budget = " << target_depth << ")" << std::endl;

    // Sequential squaring: ct = ct * ct, consuming one level per multiply
    // With depth=5, we can do 5 multiplications before exhaustion.
    auto ct_current = ct;
    for (int mult = 1; mult <= target_depth; mult++) {
        // Multiply ct_current * ct_original (not squaring, to keep values manageable)
        // Actually, let's multiply by a small plaintext constant to track easily.
        // ct = ct * 1.5  (repeated)
        std::vector<double> multiplier = {1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5};
        auto pt_mult = cc->MakeCKKSPackedPlaintext(multiplier);  // [VERIFY]
        ct_current = cc->EvalMult(ct_current, pt_mult);           // [VERIFY] ct * pt multiply

        // In FIXEDAUTO, rescale and relin happen automatically
        std::cout << "  After mult " << mult << ": level = " << ct_current->GetLevel()  // [VERIFY]
                  << std::endl;
    }

    // Decrypt and check the result
    Plaintext pt_result;
    cc->Decrypt(keys.secretKey, ct_current, &pt_result);  // [VERIFY]
    pt_result->SetLength(8);                              // [VERIFY]
    auto result_vals = pt_result->GetRealPackedValue();    // [VERIFY]

    double expected = 2.0;
    for (int i = 0; i < target_depth; i++) expected *= 1.5;
    // 2.0 * 1.5^5 = 2.0 * 7.59375 = 15.1875

    std::cout << "  Decrypted slot 0: " << result_vals[0]
              << "  (expected: " << expected << ")" << std::endl;
    double error = std::abs(result_vals[0] - expected);
    std::cout << "  Error: " << error << std::endl;
    if (error < 0.1) {
        std::cout << "  [PASS] Result within tolerance at max depth." << std::endl;
    } else {
        std::cout << "  [WARN] Precision degraded near budget limit." << std::endl;
    }
    std::cout << std::endl;

    // -----------------------------------------------------------------------
    // Part 3: Exceed the budget -- observe the failure
    // -----------------------------------------------------------------------
    // === YOUR TASK ===
    // What happens when you try one more multiplication beyond the depth budget?
    // In OpenFHE, this typically throws an exception or produces garbage output.
    // Try it and handle the error gracefully.

    std::cout << "[Part 3] Exceeding the depth budget (attempting mult " << (target_depth + 1) << "):" << std::endl;

    try {
        std::vector<double> multiplier = {1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5, 1.5};
        auto pt_extra = cc->MakeCKKSPackedPlaintext(multiplier);  // [VERIFY]
        auto ct_over = cc->EvalMult(ct_current, pt_extra);         // [VERIFY] -- this may throw

        // If it doesn't throw, the result is likely garbage
        Plaintext pt_over;
        cc->Decrypt(keys.secretKey, ct_over, &pt_over);            // [VERIFY]
        pt_over->SetLength(4);                                     // [VERIFY]
        auto over_vals = pt_over->GetRealPackedValue();            // [VERIFY]

        double expected_over = expected * 1.5;
        std::cout << "  No exception thrown, but check the result:" << std::endl;
        std::cout << "  Decrypted slot 0: " << over_vals[0]
                  << "  (expected: " << expected_over << ")" << std::endl;
        double over_error = std::abs(over_vals[0] - expected_over);
        std::cout << "  Error: " << over_error << std::endl;
        if (over_error > 1.0) {
            std::cout << "  [EXPECTED] Result is garbage -- budget exhausted, noise overwhelmed the message." << std::endl;
        } else {
            std::cout << "  [UNEXPECTED] Result still looks correct -- check if auto-rescale skipped a level." << std::endl;
        }
    } catch (const std::exception& e) {
        // [VERIFY] OpenFHE may throw openfhe_error or a derived exception type
        std::cout << "  [EXPECTED] Exception caught: " << e.what() << std::endl;
        std::cout << "  OpenFHE correctly refused the operation -- no more levels to rescale into." << std::endl;
    }
    std::cout << std::endl;

    // -----------------------------------------------------------------------
    // Part 4: The design lesson
    // -----------------------------------------------------------------------
    std::cout << "=== Design Lesson ===" << std::endl;
    std::cout << std::endl;
    std::cout << "  FHE circuit design is BACKWARDS from normal programming:" << std::endl;
    std::cout << std::endl;
    std::cout << "    Normal code:   write algorithm -> deploy" << std::endl;
    std::cout << "    FHE code:      count multiplications -> pick parameters -> write algorithm" << std::endl;
    std::cout << std::endl;
    std::cout << "  The depth budget controls EVERYTHING:" << std::endl;
    std::cout << std::endl;
    std::cout << "    Depth | Ring dim N | Approx ciphertext size | Relative speed" << std::endl;
    std::cout << "    ------|-----------|------------------------|---------------" << std::endl;
    std::cout << "      1   |   ~8192   |      ~few hundred KB   |    fast" << std::endl;
    std::cout << "      2   |  ~16384   |      ~1 MB             |    moderate" << std::endl;
    std::cout << "      5   |  ~16384   |      ~1 MB             |    moderate" << std::endl;
    std::cout << "     10   |  ~32768   |      ~5 MB             |    slow" << std::endl;
    std::cout << "     20   |  ~65536   |      ~20+ MB           |    very slow" << std::endl;
    std::cout << "    (for THIS file's settings: 128-bit security, scalingModSize=50," << std::endl;
    std::cout << "     OpenFHE's default firstModSize=60, HYBRID key switching)" << std::endl;
    std::cout << std::endl;
    std::cout << "  Why depth 2 already needs N=16384, not 8192:" << std::endl;
    std::cout << "    logQ  = firstMod + depth*scalingMod = 60 + 2*50 = 160 bits" << std::endl;
    std::cout << "    HYBRID key switching adds an auxiliary modulus P (~60 bits)," << std::endl;
    std::cout << "    and the security table is checked against logQP, not logQ:" << std::endl;
    std::cout << "    logQP ~ 220 bits > 218, the 128-bit-security cap for N=8192." << std::endl;
    std::cout << "    Twenty bits over the line costs you a doubling of the ring." << std::endl;
    std::cout << "    Forgetting P is the classic way to predict 8192 and get 16384." << std::endl;
    std::cout << std::endl;
    std::cout << "  Strategies to reduce depth:" << std::endl;
    std::cout << "    1. Tree-reduce instead of sequential (log(n) vs n depth)" << std::endl;
    std::cout << "    2. Replace deep non-polynomial functions with low-degree approximations" << std::endl;
    std::cout << "    3. Use plaintext-ciphertext multiply (costs 1 level, not ciphertext-ciphertext)" << std::endl;
    std::cout << "    4. Bootstrapping: refresh mid-circuit (expensive but removes the ceiling)" << std::endl;
    std::cout << std::endl;
    std::cout << "  For ML: this is why polynomial activation replacement matters --" << std::endl;
    std::cout << "  a degree-3 polynomial uses 2 mults, but ReLU is not polynomial at all." << std::endl;

    return 0;
}
