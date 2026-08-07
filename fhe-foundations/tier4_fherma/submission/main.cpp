/*
 * FHERMA submission skeleton — entrypoint.
 *
 * The evaluator invokes your binary with these six flags. The argument names
 * and the call sequence match templates/openfhe/main.cpp in
 * github.com/fairmath/fherma-challenges; do not rename them.
 *
 *   ./solution --cc <cryptocontext> --key_pub <public key> \
 *              --key_mult <relinearization key> --key_rot <rotation key> \
 *              --input <input ciphertext> --output <output ciphertext>
 *
 * All six are paths to OpenFHE BINARY-serialized objects. You get keys for
 * evaluation only -- there is no secret key anywhere in this process.
 */

#include <iostream>
#include <fstream>
#include <string>
#include "yourSolution.h"

using namespace lbcrypto;

int main(int argc, char *argv[])
{
    std::string pubKeyLocation;
    std::string multKeyLocation;
    std::string rotKeyLocation;
    std::string ccLocation;
    std::string inputLocation;
    std::string outputLocation;

    for (auto i = 1; i < argc; i += 2) {
        std::string arg = argv[i];
        if (i + 1 >= argc) {
            std::cerr << "Missing value for " << arg << std::endl;
            return 1;
        }
        if (arg == "--key_pub")        pubKeyLocation  = argv[i + 1];
        else if (arg == "--key_mult")  multKeyLocation = argv[i + 1];
        else if (arg == "--key_rot")   rotKeyLocation  = argv[i + 1];
        else if (arg == "--cc")        ccLocation      = argv[i + 1];
        else if (arg == "--input")     inputLocation   = argv[i + 1];
        else if (arg == "--output")    outputLocation  = argv[i + 1];
        else {
            std::cerr << "Unknown argument: " << arg << std::endl;
            return 1;
        }
    }

    if (ccLocation.empty() || pubKeyLocation.empty() || multKeyLocation.empty() ||
        rotKeyLocation.empty() || inputLocation.empty() || outputLocation.empty()) {
        std::cerr << "Usage: " << argv[0]
                  << " --cc <f> --key_pub <f> --key_mult <f> --key_rot <f>"
                     " --input <f> --output <f>" << std::endl;
        return 1;
    }

    CKKSTaskSolver solver(ccLocation, pubKeyLocation, multKeyLocation,
                          rotKeyLocation, inputLocation, outputLocation);
    solver.eval();
    solver.serializeOutput();
    return 0;
}
