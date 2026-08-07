cmake_minimum_required(VERSION 3.5.1)

project(fherma_solution CXX)
set(CMAKE_CXX_STANDARD 17)
option(BUILD_STATIC "Set to ON to include static versions of the library" OFF)

# [VERIFY] find_package(OpenFHE) needs OpenFHE installed (see Appendix B.1 of
# the book: build from source; the project publishes no official Docker image).
find_package(OpenFHE REQUIRED)

set(CMAKE_CXX_FLAGS ${OpenFHE_CXX_FLAGS})

include_directories(${OPENMP_INCLUDES})
include_directories(${OpenFHE_INCLUDE})
include_directories(${OpenFHE_INCLUDE}/third-party/include)
include_directories(${OpenFHE_INCLUDE}/core)
include_directories(${OpenFHE_INCLUDE}/pke)
include_directories(${OpenFHE_INCLUDE}/binfhe)

link_directories(${OpenFHE_LIBDIR})
link_directories(${OPENMP_LIBRARIES})

if (BUILD_STATIC)
    set(CMAKE_EXE_LINKER_FLAGS "${OpenFHE_EXE_LINKER_FLAGS} -static")
    link_libraries(${OpenFHE_STATIC_LIBRARIES})
else ()
    set(CMAKE_EXE_LINKER_FLAGS ${OpenFHE_EXE_LINKER_FLAGS})
    link_libraries(${OpenFHE_SHARED_LIBRARIES})
endif ()

add_executable(solution main.cpp yourSolution.cpp)

# Build:
#   mkdir -p build && cd build && cmake .. && make
# Run against a challenge's supplied artifacts:
#   ./solution --cc cc.bin --key_pub pub.bin --key_mult mult.bin \
#              --key_rot rot.bin --input in.bin --output out.bin
