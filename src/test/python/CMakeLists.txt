cmake_minimum_required (VERSION 3.5)
project (blob_src_test_python)

enable_testing()

add_test(NAME pythonUnitTests
  COMMAND "${CMAKE_CURRENT_SOURCE_DIR}/runUnitTests.sh" "${CMAKE_CURRENT_SOURCE_DIR}" "${CMAKE_CURRENT_SOURCE_DIR}/../../main/python")

add_custom_target(pythonTests ALL)

add_custom_command(TARGET pythonTests
  POST_BUILD
  COMMAND ctest --output-on-failure)

add_dependencies(pythonTests swig)
