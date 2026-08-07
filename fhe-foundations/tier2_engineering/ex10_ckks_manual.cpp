/*
 * Exercise 10: Explicit Rescale & Relinearize in OpenFHE CKKS
 * ============================================================
 *
 * WHAT YOU LEARN:
 *   In TenSEAL, rescaling happens automatically behind the scenes. In OpenFHE
 *   with the FIXEDMANUAL scaling technique, YOU control when it happens. This
 *   is the core CKKS engineering skill: managing scale and level bookkeeping
 *   by hand.
 *
 *   Read this carefully, because it is the single most common misconception:
 *
 *     FIXEDMANUAL controls RESCALING ONLY. It does NOT make relinearization
 *     manual. In OpenFHE, cc->EvalMult(ct1, ct2) ALREADY relinearizes
 *     internally -- the header documents it as "Homomorphic multiplication of
 *     two ciphertexts using a relinearization key" (cryptocontext.h). Its
 *     result is a normal 2-component ciphertext, so calling Relinearize() on
 *     it afterwards is wrong.
 *
 *     If you genuinely want a 3-component ciphertext -- e.g. to defer and
 *     batch relinearization, which is a real optimisation -- use
 *     EvalMultNoRelin() and then Relinearize() yourself.
 *
 *   After a ciphertext multiply:
 *     - The scale SQUARES (Delta -> Delta^2), so you MUST rescale back to Delta.
 *       Note "squares", not "doubles": it is log2(scale) that doubles. For
 *       Delta = 2^50 the product sits at 2^100, not 2^51 -- a distinction that
 *       decides whether your chain survives.
 *     - Each rescale consumes one level from your depth budget
 *     - Relinearization is already done for you unless you opted out
 *
 * WHAT YOU DO:
 *   1. Set up a CKKS context with FIXEDMANUAL scaling (no auto-rescale)
 *   2. Encrypt two vectors
 *   3. Path A: EvalMult -> Rescale (the normal workflow)
 *      Path B: EvalMultNoRelin -> Relinearize -> Rescale (manual control)
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
    // FIXEDMANUAL means OpenFHE will NOT auto-rescale for you: you call
    // Rescale() yourself after each multiply. Relinearization is NOT part of
    // this setting -- EvalMult always relinearizes unless you use
    // EvalMultNoRelin.

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
    // Try commenting out the Rescale calls to see what breaks.
    // Questions to answer:
    //   - What happens to the scale/level if you skip Rescale?
    //   - Using EvalMultNoRelin without a following Relinearize, what happens
    //     to the ciphertext size when you multiply again? Why is that costly?

    std::cout << "--- First multiplication: ct_ab = ct_a * ct_b ---" << std::endl;

    // EvalMult multiplies AND relinearizes. The result is a 2-component
    // ciphertext whose scale is Delta^2 -- under FIXEDMANUAL it is left to us
    // to rescale it back down.
    auto ct_ab = cc->EvalMult(ct_a, ct_b);
    std::cout << "  After EvalMult:        level = " << ct_ab->GetLevel()
              << ", size = " << ct_ab->GetElements().size()
              << " (already relinearized; scale is now ~Delta^2)" << std::endl;

    // Rescale: divides out one Delta, consumes one level.
    // Do NOT call Relinearize() here -- EvalMult already did it.
    ct_ab = cc->Rescale(ct_ab);
    std::cout << "  After Rescale:         level = " << ct_ab->GetLevel()
              << ", size = " << ct_ab->GetElements().size()
              << " (scale back to ~Delta)" << std::endl;
    std::cout << std::endl;

    // --- Path B: taking manual control of relinearization ------------------
    // EvalMultNoRelin leaves the degree-3 ciphertext alone so you can decide
    // when to pay for relinearization. Watch the size go 3 -> 2.
    std::cout << "--- Manual variant: EvalMultNoRelin -> Relinearize ---" << std::endl;
    auto ct_manual = cc->EvalMultNoRelin(ct_a, ct_b);
    std::cout << "  After EvalMultNoRelin: size  = " << ct_manual->GetElements().size()
              << " (3 components: c0, c1, c2)" << std::endl;
    ct_manual = cc->Relinearize(ct_manual);
    std::cout << "  After Relinearize:     size  = " << ct_manual->GetElements().size()
              << " (back to 2)" << std::endl;
    ct_manual = cc->Rescale(ct_manual);
    std::cout << "  After Rescale:         level = " << ct_manual->GetLevel() << std::endl;
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

    // NOTE: ct_ab has been rescaled once, so it sits one level below ct_a.
    // You do NOT need to level-match by hand: OpenFHE's own example says
    // "LevelReduce, and both FIXEDMANUAL and FLEXIBLEAUTO do it
    // automatically" (src/pke/examples/advanced-real-numbers.cpp), and notes
    // it costs essentially nothing. FIXEDMANUAL hands you control of
    // RESCALING only -- not level matching, and not relinearization.

    auto ct_result = cc->EvalMult(ct_ab, ct_a);   // multiplies AND relinearizes
    std::cout << "  After EvalMult:        level = " << ct_result->GetLevel()
              << ", size = " << ct_result->GetElements().size() << std::endl;

    ct_result = cc->Rescale(ct_result);
    std::cout << "  After Rescale:         level = " << ct_result->GetLevel() << std::endl;
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
    std::cout << "    EvalMult (relinearizes for you) -> Rescale   after every multiply" << std::endl;
    std::cout << "  Forget rescale        -> scale explodes, precision dies." << std::endl;
    std::cout << "  EvalMultNoRelin and then forget Relinearize" << std::endl;
    std::cout << "                        -> ciphertext bloats, next ops slow down or fail." << std::endl;
    std::cout << "  FIXEDMANUAL governs RESCALING only, never relinearization." << std::endl;

    return 0;
}
