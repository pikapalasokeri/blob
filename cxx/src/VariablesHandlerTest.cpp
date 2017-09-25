#include "catch.hpp"
#include "VariablesHandler.hpp"
#include <iostream>
#include <Eigen/Dense>

using namespace Eigen;

TEST_CASE("Default best","[VariablesHandler]")
{
  VariablesHandler handler(1.0, 1.0);
  double scale = -1.0;
  Matrix2d rotation;
  rotation << -1.0, -1.0, -1.0, -1.0;
  TranslationVector translation;
  translation << -1.0, -1.0;

  handler.getBest(scale, rotation, translation);
  REQUIRE(scale == 1.0);
  REQUIRE(rotation == Matrix2d::Identity(2, 2));
  REQUIRE(translation == MatrixXd::Zero(1, 2));
}
