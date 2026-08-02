cmake_minimum_required(VERSION 3.12)
project(fhe-tier2-exercises LANGUAGES CXX)

# -----------------------------------------------------------------------
# Find OpenFHE
# -----------------------------------------------------------------------
# [VERIFY] find_package(OpenFHE) requires OpenFHE to be installed system-wide
# or CMAKE_PREFIX_PATH to point to the OpenFHE install directory.
# If installed via `make install` to /usr/local, this should work out of the box.
# If installed elsewhere:
#   cmake .. -DCMAKE_PREFIX_PATH=/path/to/openfhe/install
find_package(OpenFHE REQUIRED)

# -----------------------------------------------------------------------
# Compiler settings
# -----------------------------------------------------------------------
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# [VERIFY] OpenFHE cmake exports these variables. Check with:
#   cmake -LH <build-dir> | grep OpenFHE
# Common variables: OpenFHE_INCLUDE, OpenFHE_LIBDIR, OpenFHE_LIBRARIES,
#                   OPENFE_INCLUDE_DIRS, OpenFHE_CXX_FLAGS
# The exact variable names depend on the OpenFHE version's CMake config.
include_directories(${OpenFHE_INCLUDE})                                       # [VERIFY] variable name
include_directories(${OpenFHE_INCLUDE}/third-party/include)                   # [VERIFY] third-party headers (cereal, etc.)
include_directories(${OpenFHE_INCLUDE}/core)                                  # [VERIFY] may be needed for some builds
include_directories(${OpenFHE_INCLUDE}/pke)                                   # [VERIFY] may be needed for some builds
link_directories(${OpenFHE_LIBDIR})                                           # [VERIFY] variable name

# [VERIFY] OpenFHE may export compiler flags; apply them if available
if(OpenFHE_CXX_FLAGS)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenFHE_CXX_FLAGS}")           # [VERIFY] variable name
endif()

# -----------------------------------------------------------------------
# Exercise executables
# -----------------------------------------------------------------------

# Exercise 10: Manual rescale and relinearize in CKKS
add_executable(ex10_ckks_manual ex10_ckks_manual.cpp)
target_link_libraries(ex10_ckks_manual ${OpenFHE_LIBRARIES})                  # [VERIFY] link variable

# Exercise 11: Rotations, slot summation, packed matrix-vector product
add_executable(ex11_rotations ex11_rotations.cpp)
target_link_libraries(ex11_rotations ${OpenFHE_LIBRARIES})                    # [VERIFY] link variable

# Exercise 12: Depth budget, parameter selection, budget exhaustion
add_executable(ex12_depth_budget ex12_depth_budget.cpp)
target_link_libraries(ex12_depth_budget ${OpenFHE_LIBRARIES})                 # [VERIFY] link variable

# -----------------------------------------------------------------------
# Build instructions
# -----------------------------------------------------------------------
# To build:
#   mkdir build && cd build
#   cmake ..                             # or: cmake .. -DCMAKE_PREFIX_PATH=/path/to/openfhe
#   make
#
# To run:
#   ./ex10_ckks_manual
#   ./ex11_rotations
#   ./ex12_depth_budget
#
# [VERIFY] If linking fails, check that OpenFHE was built with shared libraries:
#   cmake .. -DBUILD_SHARED=ON   (in the OpenFHE build itself)
# and that LD_LIBRARY_PATH includes the OpenFHE lib directory at runtime.
