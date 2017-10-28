cmake_minimum_required (VERSION 2.6)
project (pointmatcher)

set(PROJECT_SOURCE_DIR src)

find_package(Boost 1.55)

IF(CMAKE_COMPILER_IS_GNUCXX)
    SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Werror -Wno-deprecated -std=c++11 -fopenmp")
ENDIF(CMAKE_COMPILER_IS_GNUCXX)

include_directories(${Boost_INCLUDE_DIR}
                    "${PROJECT_SOURCE_DIR}/Eigen")

add_library(cxxblob SHARED
  "${PROJECT_SOURCE_DIR}/Utilities.cpp"
  "${PROJECT_SOURCE_DIR}/SimulatedAnnealingPointMatcher2D.cpp"
  "${PROJECT_SOURCE_DIR}/CoherentPointDriftMatcher2D.cpp"
  "${PROJECT_SOURCE_DIR}/RigidSolver.cpp"
  "${PROJECT_SOURCE_DIR}/VariablesHandler.cpp"
  "${PROJECT_SOURCE_DIR}/MostPopulatedCircleFinder.cpp"
  "${PROJECT_SOURCE_DIR}/MeanShortestDistanceFitnessComputer.cpp"
)

set(CMAKE_BUILD_TYPE Release)



enable_testing()

add_executable(catchTests
  "${PROJECT_SOURCE_DIR}/test.cpp"
  "${PROJECT_SOURCE_DIR}/VariablesHandlerTest.cpp"
  "${PROJECT_SOURCE_DIR}/MostPopulatedCircleFinderTest.cpp"
  "${PROJECT_SOURCE_DIR}/MeanShortestDistanceFitnessComputerTest.cpp"
)

target_link_libraries(catchTests
  cxxblob)

add_test(NAME catchUnitTests
  COMMAND catchTests)

add_custom_command(TARGET catchTests
  POST_BUILD
  COMMAND ctest --output-on-failure)
