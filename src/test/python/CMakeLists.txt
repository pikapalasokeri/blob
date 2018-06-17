cmake_minimum_required (VERSION 3.5)
project (blob_src_test_python)

enable_testing()

add_test(NAME pythonUnitTests
  COMMAND "${CMAKE_CURRENT_SOURCE_DIR}/runUnitTests.sh" "${CMAKE_CURRENT_SOURCE_DIR}" "${CMAKE_CURRENT_SOURCE_DIR}/../../main/python")

# E501 line too long (X > 79 characters)
set(FLAKE8_IGNORE_LIST "E501")
add_test(NAME pythonFlake8Test
  COMMAND "flake8" "--ignore=${FLAKE8_IGNORE_LIST}" "${CMAKE_CURRENT_SOURCE_DIR}/../../main/python")

add_custom_target(pythonTests ALL)

add_custom_command(TARGET pythonTests
  POST_BUILD
  COMMAND ctest --output-on-failure)

add_dependencies(pythonTests swig)
