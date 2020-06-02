cmake_minimum_required (VERSION 3.5)
project (blob_src_main_swig)

set(PROJECT_SOURCE_DIR .)
find_package(SWIG REQUIRED)
find_package(PythonLibs 3 REQUIRED)

include(${SWIG_USE_FILE})

IF(CMAKE_COMPILER_IS_GNUCXX)
    SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Werror -Wno-ignored-attributes -Wno-deprecated -std=c++11 -fopenmp -O3")
ENDIF(CMAKE_COMPILER_IS_GNUCXX)

include_directories(
  ${PYTHON_INCLUDE_DIRS}
  "${PROJECT_SOURCE_DIR}/../cxx/"
  "${PROJECT_SOURCE_DIR}/../cxx/Eigen"
  ${PROJECT_SOURCE_DIR}
  )

set_property(SOURCE "${PROJECT_SOURCE_DIR}/MostPopulatedCircleFinder.i" PROPERTY CPLUSPLUS ON)
swig_add_module(MostPopulatedCircleFinder python "${PROJECT_SOURCE_DIR}/MostPopulatedCircleFinder.i")
swig_link_libraries(MostPopulatedCircleFinder blob)

set_property(SOURCE "${PROJECT_SOURCE_DIR}/CoherentPointDriftMatcher2D.i" PROPERTY CPLUSPLUS ON)
swig_add_module(CoherentPointDriftMatcher2D python "${PROJECT_SOURCE_DIR}/CoherentPointDriftMatcher2D.i")
swig_link_libraries(CoherentPointDriftMatcher2D blob)

set_property(SOURCE "${PROJECT_SOURCE_DIR}/SimulatedAnnealingPointMatcher2D.i" PROPERTY CPLUSPLUS ON)
swig_add_module(SimulatedAnnealingPointMatcher2D python "${PROJECT_SOURCE_DIR}/SimulatedAnnealingPointMatcher2D.i")
swig_link_libraries(SimulatedAnnealingPointMatcher2D blob)

set_property(SOURCE "${PROJECT_SOURCE_DIR}/BruteForceMatcher.i" PROPERTY CPLUSPLUS ON)
swig_add_module(BruteForceMatcher python "${PROJECT_SOURCE_DIR}/BruteForceMatcher.i")
swig_link_libraries(BruteForceMatcher blob)

set_property(SOURCE "${PROJECT_SOURCE_DIR}/MeanShortestDistanceFitnessComputer.i" PROPERTY CPLUSPLUS ON)
swig_add_module(MeanShortestDistanceFitnessComputer python "${PROJECT_SOURCE_DIR}/MeanShortestDistanceFitnessComputer.i")
swig_link_libraries(MeanShortestDistanceFitnessComputer blob)

set_property(SOURCE "${PROJECT_SOURCE_DIR}/AbsoluteNeighborFitnessComputer.i" PROPERTY CPLUSPLUS ON)
swig_add_module(AbsoluteNeighborFitnessComputer python "${PROJECT_SOURCE_DIR}/AbsoluteNeighborFitnessComputer.i")
swig_link_libraries(AbsoluteNeighborFitnessComputer blob)

set(SWIG_TARGETS
  ${SWIG_MODULE_MostPopulatedCircleFinder_REAL_NAME}
  ${SWIG_MODULE_CoherentPointDriftMatcher2D_REAL_NAME}
  ${SWIG_MODULE_SimulatedAnnealingPointMatcher2D_REAL_NAME}
  ${SWIG_MODULE_BruteForceMatcher_REAL_NAME}
  ${SWIG_MODULE_MeanShortestDistanceFitnessComputer_REAL_NAME}
  ${SWIG_MODULE_AbsoluteNeighborFitnessComputer_REAL_NAME})

add_custom_target(swig)
add_dependencies(swig ${SWIG_TARGETS})

install(TARGETS
  ${SWIG_TARGETS}
  LIBRARY DESTINATION ${INSTALL_DIR}/lib)

set(SWIG_OUTDIR "${CMAKE_BINARY_DIR}/src/main/swig")
install(FILES
  ${SWIG_OUTDIR}/MostPopulatedCircleFinder.py
  ${SWIG_OUTDIR}/CoherentPointDriftMatcher2D.py
  ${SWIG_OUTDIR}/SimulatedAnnealingPointMatcher2D.py
  ${SWIG_OUTDIR}/BruteForceMatcher.py
  ${SWIG_OUTDIR}/MeanShortestDistanceFitnessComputer.py
  ${SWIG_OUTDIR}/AbsoluteNeighborFitnessComputer.py
  DESTINATION ${INSTALL_DIR}/python)
