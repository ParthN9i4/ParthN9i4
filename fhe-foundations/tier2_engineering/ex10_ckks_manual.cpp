/*
 * Exercise 10: Explicit Rescale & Relinearize in OpenFHE CKKS
 * ============================================================
 *
 * WHAT YOU LEARN:
 *   In TenSEAL, rescale and relinearize happen automatically behind the scenes.
 *   In OpenFHE with FIXEDMANUAL scaling technique, YOU control when rescale and
 *   relinearize happen. This is the core CKKS engineering skill: managing scale
 *   and level bookkeeping by hand.
 *
 *   After a ciphertext multiply:
 *     - The scale doubles (Delta^2), so you MUST rescale to bring it back to Delta
 *     - The ciphertext grows from 2 to 3 components, so you MUST relinearize
 *     - Each rescale consumes one level from your depth budget
 *
 * WHAT YOU DO:
 *   1. Set up a CKKS context with FIXEDMANUAL scaling (no auto-rescale)
 *   2. Encrypt two vectors
 *   3. Multiply -> rescale -> relinearize -> multiply again -> rescale -> relin
 *   4. Track and print the level after each operation
 *   5. Decrypt and verify against plaintext computation
 *
 * BUILD:
 *   mkdir build && cd build && cmake .. && make ex10_ckks_manual
 *   ./ex10_ckks_manual
 */

#include "openfhe.h"                    // [VERIFY] main OpenFHE header
using namespace lbcrypto;               // [VERIFY] OpenFHE namespace

int main() {
    std::cout << "=== Exercise 10: Manual Rescale & Relinearize in CKKS ===" << std::endl;
    std::cout << std::endl;

    // -----------------------------------------------------------------------
    // Step 1: Set up CryptoContext with FIXEDMANUAL scaling
    // -----------------------------------------------------------------------
    // FIXEDMANUAL means OpenFHE will NOT auto-rescale or auto-relin for you.
    // You must call Rescale() and Relinearize() yourself after each multiply.

    CCParams<CryptoContextCKKSRNS> parameters;         // [VERIFY] parameter class name
    parameters.SetMultiplicativeDepth(3);               // [VERIFY] method name
    parameters.SetScalingModSize(50);                   // [VERIFY] method name; sets each qi ~50 bits
    parameters.SetBatchSize(8);                         // [VERIFY] method name; number of CKKS slots to use
    parameters.SetScalingTechnique(FIXEDMANUAL);        // [VERIFY] enum value for manual scaling

    auto cc = GenCryptoContext(parameters);             // [VERIFY] factory function
    cc->Enable(PKE);                                    // [VERIFY] enable public-key encryption
    cc->Enable(KEYSWITCH);                              // [VERIFY] enable key switching (needed for relin)
    cc->Enable(LEVELEDSHE);                             // [VERIFY] enable leveled SHE operations

    std::cout << "[Setup] CryptoContext created." << std::endl;
    std::cout << "  Multiplicative depth: 3" << std::endl;
    std::cout << "  Scaling mod size:     50 bits" << std::endl;
    std::cout << "  Scaling technique:    FIXEDMANUAL" << std::endl;
    std::cout << "  Ring dimension N:     " << cc->GetRingDimension() << std::endl;  // [VERIFY]
    std::cout << std::endl;

    // -----------------------------------------------------------------------
    // Step 2: Key generation
    // -----------------------------------------------------------------------
    auto keys = cc->KeyGen();                           // [VERIFY] returns KeyPair
    cc->EvalMultKeyGen(keys.secretKey);                 // [VERIFY] generate relinearization key

    std::cout << "[KeyGen] Public key, secret key, and relinearization key generated." << std::endl;
    std::cout << std::endl;

    // -----------------------------------------------------------------------
    // Step 3: Encode and encrypt two vectors
    // -----------------------------------------------------------------------
    // CKKS packs up to N/2 slots; we use 8 here for readability.
    std::vector<double> vec_a = {1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0};
    std::vector<double> vec_b = {0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5};

    // MakeCKKSPackedPlaintext encodes a vector into a CKKS plaintext
    auto pt_a = cc->MakeCKKSPackedPlaintext(vec_a);     // [VERIFY] method name and signature
    auto pt_b = cc->MakeCKKSPackedPlaintext(vec_b);     // [VERIFY]

    auto ct_a = cc->Encrypt(keys.publicKey, pt_a);      // [VERIFY] Encrypt signature
    auto ct_b = cc->Encrypt(keys.publicKey, pt_b);      // [VERIFY]

    std::cout << "[Encrypt] Two vectors encrypted." << std::endl;
    std::cout << "  vec_a = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]" << std::endl;
    std::cout << "  vec_b = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5]" << std::endl;
    std::cout << "  Level after encryption: " << ct_a->GetLevel() << std::endl;  // [VERIFY] GetLevel()
    std::cout << std::endl;

    // -----------------------------------------------------------------------
    // Step 4: First multiply -> rescale -> relinearize
    // -----------------------------------------------------------------------
    // === YOUR TASK ===
    // Try commenting out the Rescale or Relinearize calls to see what breaks.
    // Questions to answer:
    //   - What happens to the level if you skip Rescale?
    //   - What happens to subsequent multiplies if you skip Relinearize?

    std::cout << "--- First multiplication: ct_ab = ct_a * ct_b ---" << std::endl;

    // Multiply: result has scale Delta^2 and ciphertext size 3
    auto ct_ab = cc->EvalMult(ct_a, ct_b);              // [VERIFY] EvalMult signature
    std::cout << "  After EvalMult:        level = " << ct_ab->GetLevel()
              << " (ciphertext has 3 components now)" << std::endl;

    // Rescale: divides out one Delta, consumes one level
    ct_ab = cc->Rescale(ct_ab);                          // [VERIFY] Rescale signature (may be ModReduce in some versions)
    std::cout << "  After Rescale:         level = " << ct_ab->GetLevel()
              << " (scale back to ~Delta)" << std::endl;

    // Relinearize: reduces ciphertext from 3 components back to 2
    ct_ab = cc->Relinearize(ct_ab);                      // [VERIFY] Relinearize signature
    std::cout << "  After Relinearize:     level = " << ct_ab->GetLevel()
              << " (ciphertext back to 2 components)" << std::endl;
    std::cout << std::endl;

    // -----------------------------------------------------------------------
    // Step 5: Second multiply -> rescale -> relinearize
    // -----------------------------------------------------------------------
    // We multiply ct_ab * ct_a to get a * b * a = a^2 * b
    std::cout << "--- Second multiplication: ct_result = ct_ab * ct_a ---" << std::endl;

    // === YOUR TASK ===
    // Before this multiply, ct_ab is at a lower level than ct_a.
    // In FIXEDMANUAL mode, you may need to bring ct_a to the same level.
    // Think about why: operands must share the same scale and level.

    // NOTE: In FIXEDMANUAL, you may need to level-match ct_a down to ct_ab's level.
    // OpenFHE's EvalMult may handle this internally, or you may need:
    //   cc->LevelReduce(ct_a, nullptr, ct_ab->GetLevel() - ct_a->GetLevel());
    // [VERIFY] Check whether EvalMult auto-adjusts levels or requires manual LevelReduce

    auto ct_result = cc->EvalMult(ct_ab, ct_a);          // [VERIFY]
    std::cout << "  After EvalMult:        level = " << ct_result->GetLevel() << std::endl;

    ct_result = cc->Rescale(ct_result);                   // [VERIFY]
    std::cout << "  After Rescale:         level = " << ct_result->GetLevel() << std::endl;

    ct_result = cc->Relinearize(ct_result);               // [VERIFY]
    std::cout << "  After Relinearize:     level = " << ct_result->GetLevel() << std::endl;
    std::cout << std::endl;

    // -----------------------------------------------------------------------
    // Step 6: Decrypt and verify
    // -----------------------------------------------------------------------
    Plaintext pt_result;                                  // [VERIFY] Plaintext type
    cc->Decrypt(keys.secretKey, ct_result, &pt_result);   // [VERIFY] Decrypt signature (output param)
    pt_result->SetLength(8);                              // [VERIFY] truncate to our batch size

    auto result_vec = pt_result->GetRealPackedValue();    // [VERIFY] GetRealPackedValue method

    // Compute expected result in plaintext: a * b * a = a^2 * b
    std::cout << "[Verify] Comparing decrypted result to plaintext computation:" << std::endl;
    std::cout << "  Expected (a^2 * b) vs Decrypted:" << std::endl;

    double max_error = 0.0;
    for (size_t i = 0; i < vec_a.size(); i++) {
        double expected = vec_a[i] * vec_b[i] * vec_a[i];
        double actual   = result_vec[i];
        double error    = std::abs(expected - actual);
        max_error = std::max(max_error, error);
        std::cout << "    slot " << i << ": expected = " << expected
                  << ", got = " << actual
                  << ", error = " << error << std::endl;
    }

    std::cout << std::endl;
    std::cout << "  Max error: " << max_error << std::endl;
    if (max_error < 0.01) {
        std::cout << "  [PASS] Result matches within CKKS approximation tolerance." << std::endl;
    } else {
        std::cout << "  [FAIL] Error too large -- check rescale/relin sequence." << std::endl;
    }

    // -----------------------------------------------------------------------
    // Summary of level consumption
    // -----------------------------------------------------------------------
    std::cout << std::endl;
    std::cout << "=== Level Budget Summary ===" << std::endl;
    std::cout << "  Starting depth budget:       3" << std::endl;
    std::cout << "  Levels consumed by multiply: 2 (one rescale per multiply)" << std::endl;
    std::cout << "  Remaining levels:            1" << std::endl;
    std::cout << "  -> One more multiply would be possible, then the budget is exhausted." << std::endl;
    std::cout << std::endl;
    std::cout << "=== Key Takeaway ===" << std::endl;
    std::cout << "  In FIXEDMANUAL mode, YOU are the compiler:" << std::endl;
    std::cout << "    multiply -> rescale -> relinearize   (in that order, every time)" << std::endl;
    std::cout << "  Forget rescale -> scale explodes, precision dies." << std::endl;
    std::cout << "  Forget relin   -> ciphertext bloats, next ops fail or slow down." << std::endl;

    return 0;
}
