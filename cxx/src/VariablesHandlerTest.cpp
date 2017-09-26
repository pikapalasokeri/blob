#include "catch.hpp"
#include "VariablesHandler.hpp"
#include "TestUtilities.hpp"

#include <iostream>
#include <Eigen/Dense>

using namespace Eigen;


TEST_CASE("Default best","[VariablesHandler]")
{
  VariablesHandler handler(1.0, 1.0);
  double scale = -1.0;
  Matrix2d rotation;
  TranslationVector translation;

  rotation << -1.0, -1.0, -1.0, -1.0;
  translation << -1.0, -1.0;

  handler.getBest(scale, rotation, translation);
  CHECK(scale == 1.0);
  CHECK(rotation == Matrix2d::Identity(2, 2));
  CHECK(translation == MatrixXd::Zero(1, 2));
}

TEST_CASE("Single proposeNewVariables", "[VariablesHandler]")
{
  VariablesHandler handler(360.0, 10.0);
  double scale = -1.0;
  Matrix2d rotation;
  TranslationVector translation;

  handler.proposeNewVariables(scale, rotation, translation);

  CHECK(scale == 1.0);

  CHECK(isRotationMatrix(rotation));
  Matrix2d expectedRotation;
  expectedRotation <<  0.911943, 0.410316,
                      -0.410316, 0.911943;
  CHECK(closeEnough(rotation, expectedRotation));

  TranslationVector expectedTranslation;
  expectedTranslation << -12.015, -4.37855;
  CHECK(closeEnough(translation, expectedTranslation));
}


