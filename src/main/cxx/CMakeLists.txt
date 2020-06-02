cmake_minimum_required (VERSION 3.5)
project (blob_src_main_cxx)

set(PROJECT_SOURCE_DIR .)

IF(CMAKE_COMPILER_IS_GNUCXX)
    SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Werror -Wno-ignored-attributes -Wno-deprecated -std=c++11 -fopenmp -O3")
ENDIF(CMAKE_COMPILER_IS_GNUCXX)

include_directories(
  "${PROJECT_SOURCE_DIR}/Eigen"
  ${PROJECT_SOURCE_DIR}
  )

add_library(blob SHARED
  "${PROJECT_SOURCE_DIR}/Utilities.cpp"
  "${PROJECT_SOURCE_DIR}/SimulatedAnnealingPointMatcher2D.cpp"
  "${PROJECT_SOURCE_DIR}/CoherentPointDriftMatcher2D.cpp"
  "${PROJECT_SOURCE_DIR}/RigidSolver.cpp"
  "${PROJECT_SOURCE_DIR}/VariablesHandler.cpp"
  "${PROJECT_SOURCE_DIR}/MostPopulatedCircleFinder.cpp"
  "${PROJECT_SOURCE_DIR}/MeanShortestDistanceFitnessComputer.cpp"
  "${PROJECT_SOURCE_DIR}/AbsoluteNeighborFitnessComputer.cpp"
  "${PROJECT_SOURCE_DIR}/BruteForceMatcher.cpp"
)

set(CMAKE_BUILD_TYPE Release)

install(TARGETS blob
        LIBRARY DESTINATION ${INSTALL_DIR}/lib)
