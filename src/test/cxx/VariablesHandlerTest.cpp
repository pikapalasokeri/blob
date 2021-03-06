#include "catch.hpp"
#include "VariablesHandler.hpp"
#include "TestUtilities.hpp"

TEST_CASE("Default best","[VariablesHandler]")
{
  VariablesHandler handler(1.0, 1.0);
  double scale = -1.0;
  RotationMatrix rotation;
  TranslationVector translation;

  rotation << -1.0, -1.0, -1.0, -1.0;
  translation << -1.0, -1.0;

  handler.getBest(scale, rotation, translation);
  CHECK(scale == 1.0);
  CHECK(rotation == RotationMatrix::Identity(2, 2));
  CHECK(translation == TranslationVector::Zero(1, 2));
}

TEST_CASE("Single proposeNewVariables", "[VariablesHandler]")
{
  VariablesHandler handler(360.0, 10.0);
  double scale = -1.0;
  RotationMatrix rotation;
  TranslationVector translation;

  handler.proposeNewVariables(scale, rotation, translation);

  CHECK(scale == 1.0);

  CHECK(isRotationMatrix(rotation));
  RotationMatrix expectedRotation;
  expectedRotation <<  0.911943, 0.410316,
                      -0.410316, 0.911943;
  CHECK_THAT(rotation, isCloseEnoughTo(expectedRotation));

  TranslationVector expectedTranslation;
  expectedTranslation << -12.015, -4.37855;
  CHECK_THAT(translation, isCloseEnoughTo(expectedTranslation));
}

TEST_CASE("acceptProposed, setCurrentIsBest", "[VariablesHandler]")
{
  VariablesHandler handler(360.0, 10.0);
  double proposedScale = -1.0;
  RotationMatrix proposedRotation;
  TranslationVector proposedTranslation;

  handler.proposeNewVariables(proposedScale, proposedRotation, proposedTranslation);
  handler.acceptProposed();
  handler.setCurrentIsBest();

  double bestScale = -1.0;
  RotationMatrix bestRotation;
  TranslationVector bestTranslation;
  handler.getBest(bestScale, bestRotation, bestTranslation);

  CHECK(bestScale == proposedScale);
  CHECK_THAT(bestRotation, isCloseEnoughTo(proposedRotation, 1.0e-15));
  CHECK_THAT(bestTranslation, isCloseEnoughTo(proposedTranslation, 1.0e-15));
}

TEST_CASE("setBestAsCurrent", "[VariablesHandler]")
{
  VariablesHandler handler(360.0, 10.0);
  double proposedScale = -1.0;
  RotationMatrix proposedRotation;
  TranslationVector proposedTranslation;
  double newProposedScale = -1.0;
  RotationMatrix newProposedRotation;
  TranslationVector newProposedTranslation;

  handler.proposeNewVariables(proposedScale, proposedRotation, proposedTranslation);
  handler.acceptProposed(); // current is now proposed
  handler.setCurrentIsBest(); // best is now proposed
  handler.proposeNewVariables(newProposedScale, newProposedRotation, newProposedTranslation);
  handler.acceptProposed(); // current is now new proposed
  handler.setBestAsCurrent(); // current is now best = proposed
  handler.setCurrentIsBest(); // best is now proposed

  double bestScale = -1.0;
  RotationMatrix bestRotation;
  TranslationVector bestTranslation;
  handler.getBest(bestScale, bestRotation, bestTranslation);

  CHECK(bestScale == proposedScale);
  CHECK_THAT(bestRotation, isCloseEnoughTo(proposedRotation, 1.0e-15));
  CHECK_THAT(bestTranslation, isCloseEnoughTo(proposedTranslation, 1.0e-15));
}

TEST_CASE("setRotationSigma, setTranslationSigma", "[VariablesHandler]")
{
  VariablesHandler handler(360.0, 10.0);
  handler.setRotationSigma(0.0);
  handler.setTranslationSigma(0.0);
  double scale = -1.0;
  RotationMatrix rotation;
  TranslationVector translation;

  handler.proposeNewVariables(scale, rotation, translation);

  CHECK(scale == 1.0);

  CHECK(isRotationMatrix(rotation));
  RotationMatrix expectedRotation;
  expectedRotation <<  1.0, 0.0,
                       0.0, 1.0;
  CHECK_THAT(rotation, isCloseEnoughTo(expectedRotation));

  TranslationVector expectedTranslation;
  expectedTranslation << 0.0, 0.0;
  CHECK_THAT(translation, isCloseEnoughTo(expectedTranslation));
}



