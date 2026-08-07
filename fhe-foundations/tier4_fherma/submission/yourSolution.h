/*
 * FHERMA submission skeleton — solver class.
 *
 * The class name, constructor signature, and the eval()/serializeOutput()
 * entry points mirror templates/openfhe/yourSolution.h in
 * github.com/fairmath/fherma-challenges. Keep them as-is: main.cpp and the
 * evaluator both depend on this shape. Put YOUR work in eval().
 *
 * The threat model is the whole point: you receive a CryptoContext, a public
 * key, an evaluation (relinearization) key, a rotation key, and one input
 * ciphertext. You never see plaintext and you have no secret key. Anything
 * that would require decrypting an intermediate is not available to you.
 */

#include "openfhe.h"

#include "ciphertext-ser.h"
#include "cryptocontext-ser.h"
#include "key/key-ser.h"
#include "scheme/ckksrns/ckksrns-ser.h"

using namespace lbcrypto;

class CKKSTaskSolver {
    CryptoContext<DCRTPoly> m_cc;
    PublicKey<DCRTPoly> m_PublicKey;
    Ciphertext<DCRTPoly> m_InputC;
    Ciphertext<DCRTPoly> m_OutputC;
    std::string m_PubKeyLocation;
    std::string m_MultKeyLocation;
    std::string m_RotKeyLocation;
    std::string m_CCLocation;
    std::string m_InputLocation;
    std::string m_OutputLocation;

public:
    CKKSTaskSolver(std::string ccLocation, std::string pubKeyLocation,
                   std::string multKeyLocation, std::string rotKeyLocation,
                   std::string inputLocation, std::string outputLocation);

    void initCC();

    // === YOUR TASK ===
    // Read m_InputC, compute homomorphically, leave the result in m_OutputC.
    void eval();

    void serializeOutput();
};
