cmake_minimum_required (VERSION 3.5)
project (blob_src_test_performance)

enable_testing()

# E501 line too long (X > 79 characters)
set(FLAKE8_IGNORE_LIST "E501")
add_test(NAME pythonFlake8Test
  COMMAND "flake8" "--ignore=${FLAKE8_IGNORE_LIST}"
  "${CMAKE_CURRENT_SOURCE_DIR}/../../test/performance")

add_custom_target(performanceTests)

add_custom_command(TARGET performanceTests
  POST_BUILD
  COMMAND ctest --output-on-failure
  COMMAND "${CMAKE_CURRENT_SOURCE_DIR}/runPerformanceTests.sh" "${CMAKE_CURRENT_SOURCE_DIR}" "${CMAKE_CURRENT_SOURCE_DIR}/../../main/python")

add_dependencies(performanceTests swig)
