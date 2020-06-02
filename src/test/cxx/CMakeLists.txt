cmake_minimum_required (VERSION 3.5)
project (blob_src_test_cxx)

set(PROJECT_SOURCE_DIR ".")

IF(CMAKE_COMPILER_IS_GNUCXX)
    SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Werror -Wno-ignored-attributes -Wno-deprecated -std=c++11 -fopenmp -O3")
ENDIF(CMAKE_COMPILER_IS_GNUCXX)

include_directories(
  "${PROJECT_SOURCE_DIR}/../../main/cxx/Eigen"
  "${PROJECT_SOURCE_DIR}/../../main/cxx"
  )

set(CMAKE_BUILD_TYPE Release)

enable_testing()

add_executable(catchTests
  "${PROJECT_SOURCE_DIR}/test.cpp"
  "${PROJECT_SOURCE_DIR}/VariablesHandlerTest.cpp"
  "${PROJECT_SOURCE_DIR}/MostPopulatedCircleFinderTest.cpp"
  "${PROJECT_SOURCE_DIR}/MeanShortestDistanceFitnessComputerTest.cpp"
  "${PROJECT_SOURCE_DIR}/AbsoluteNeighborFitnessComputerTest.cpp"
)

target_link_libraries(catchTests
  blob)

add_test(NAME catchUnitTests
  COMMAND catchTests)

add_custom_target(tests ALL)

add_custom_command(TARGET tests
  POST_BUILD
  COMMAND ctest --output-on-failure)

add_dependencies(tests catchTests)
