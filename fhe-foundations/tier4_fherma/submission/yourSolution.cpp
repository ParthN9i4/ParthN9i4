/*
 * FHERMA submission skeleton — implementation.
 *
 * initCC() and serializeOutput() are boilerplate that matches the official
 * template; you should not need to change them. eval() is yours.
 *
 * Every OpenFHE call below is marked [VERIFY] where its exact signature is
 * worth re-checking against the version you build against, per the
 * no-hallucinated-APIs rule that governs this whole exercise ladder.
 */

#include "yourSolution.h"

CKKSTaskSolver::CKKSTaskSolver(std::string ccLocation, std::string pubKeyLocation,
                               std::string multKeyLocation, std::string rotKeyLocation,
                               std::string inputLocation, std::string outputLocation)
    : m_PubKeyLocation(pubKeyLocation),
      m_MultKeyLocation(multKeyLocation),
      m_RotKeyLocation(rotKeyLocation),
      m_CCLocation(ccLocation),
      m_InputLocation(inputLocation),
      m_OutputLocation(outputLocation)
{
    initCC();
}

void CKKSTaskSolver::initCC()
{
    if (!Serial::DeserializeFromFile(m_CCLocation, m_cc, SerType::BINARY)) {
        std::cerr << "Could not deserialize cryptocontext file" << std::endl;
        std::exit(1);
    }

    if (!Serial::DeserializeFromFile(m_PubKeyLocation, m_PublicKey, SerType::BINARY)) {
        std::cerr << "Could not deserialize public key file" << std::endl;
        std::exit(1);
    }

    std::ifstream multKeyIStream(m_MultKeyLocation, std::ios::in | std::ios::binary);
    if (!multKeyIStream.is_open() ||
        !m_cc->DeserializeEvalMultKey(multKeyIStream, SerType::BINARY)) {
        std::cerr << "Could not deserialize eval mult key file" << std::endl;
        std::exit(1);
    }

    std::ifstream rotKeyIStream(m_RotKeyLocation, std::ios::in | std::ios::binary);
    if (!rotKeyIStream.is_open() ||
        !m_cc->DeserializeEvalAutomorphismKey(rotKeyIStream, SerType::BINARY)) {
        std::cerr << "Could not deserialize eval rotation key file" << std::endl;
        std::exit(1);
    }

    if (!Serial::DeserializeFromFile(m_InputLocation, m_InputC, SerType::BINARY)) {
        std::cerr << "Could not deserialize input ciphertext" << std::endl;
        std::exit(1);
    }
}

void CKKSTaskSolver::eval()
{
    // ======================= YOUR SOLUTION GOES HERE =======================
    //
    // Worked example: apply a polynomial approximation of an activation to
    // every slot. This is the shape most activation challenges take, and it
    // is where a Chebyshev/minimax fit earns its score.
    //
    // Replace `targetFn` and `degree` with the challenge's function and the
    // lowest degree that meets its accuracy bar. Lower degree means fewer
    // levels, which means a smaller ring, which means a faster run -- that
    // chain is the whole optimisation.

    const double lowerBound = -8.0;   // the challenge's stated input range
    const double upperBound = 8.0;
    const uint32_t degree = 7;        // tune: lowest degree meeting the bar

    auto targetFn = [](double x) -> double {
        return 1.0 / (1.0 + std::exp(-x));   // sigmoid; swap for the real target
    };

    // EvalChebyshevFunction fits and evaluates in one call, using
    // Paterson-Stockmeyer internally. [VERIFY] signature.
    //
    // DEPTH WARNING: this costs MORE than ceil(log2(degree+1)). Per OpenFHE's
    // FUNCTION_EVALUATION.md, degree 6-13 costs 5 levels and degree 14-27
    // costs 6. Declare mult_depth in config.json from that table -- use
    // ../fherma_config.py to compute it. Under-declaring is the most common
    // reason a submission that works locally dies in the evaluator.
    m_OutputC = m_cc->EvalChebyshevFunction(targetFn, m_InputC,
                                            lowerBound, upperBound, degree);

    // --- Common patterns you may need, and their costs --------------------
    //
    // Sum all slots (log-reduce). Every offset used here must appear in
    // config.json's indexes_for_rotation_key, or EvalRotate throws:
    //   auto acc = m_OutputC;
    //   for (int k = 1; k < batchSize; k <<= 1)
    //       acc = m_cc->EvalAdd(acc, m_cc->EvalRotate(acc, k));
    //
    // Multiply by a plaintext vector -- COSTS ONE LEVEL, it is not free:
    //   auto pt = m_cc->MakeCKKSPackedPlaintext(weights);
    //   m_OutputC = m_cc->EvalMult(m_OutputC, pt);
    //
    // Ciphertext multiply: EvalMult relinearizes for you. Use
    // EvalMultNoRelin only if you intend to defer relinearization yourself.
    //
    // =======================================================================
}

void CKKSTaskSolver::serializeOutput()
{
    if (!Serial::SerializeToFile(m_OutputLocation, m_OutputC, SerType::BINARY)) {
        std::cerr << "Could not serialize output ciphertext" << std::endl;
        std::exit(1);
    }
}
