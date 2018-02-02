#include "VariablesHandler.hpp"

VariablesHandler::VariablesHandler(double rotationSigma,
                                   double translationSigma)
  : rotationSigma_(rotationSigma),
    translationSigma_(translationSigma),
    pi_(cos(-1.0))
{
  currentScale_ = 1.0;
  currentRotation_ << 1.0, 0.0,
                      0.0, 1.0;
  currentTranslation_ << 0.0, 0.0;

  bestScale_ = 1.0;
  bestRotation_ = currentRotation_;
  bestTranslation_ = currentTranslation_;
}

void
VariablesHandler::proposeNewVariables(double& scale,
                                      RotationMatrix& rotation,
                                      TranslationVector& translation)
{
  proposedScale_ = 1.0;

  const double rotationDegrees = normalRandomGenerator_.getNext() * rotationSigma_;
  const double rotationRadians = pi_ / 180.0 * rotationDegrees;
  const double cosRotation = cos(rotationRadians);
  const double sinRotation = sin(rotationRadians);
  RotationMatrix thisRotation;
  thisRotation << cosRotation, -sinRotation,
                  sinRotation,  cosRotation;
  proposedRotation_ = thisRotation * currentRotation_;

  const double translationX = normalRandomGenerator_.getNext() * translationSigma_;
  const double translationY = normalRandomGenerator_.getNext() * translationSigma_;
  TranslationVector thisTranslation;
  thisTranslation << translationX, translationY;
  proposedTranslation_ = thisTranslation + currentTranslation_;

  scale = proposedScale_;
  rotation = proposedRotation_;
  translation = proposedTranslation_;
}

void
VariablesHandler::acceptProposed()
{
  currentScale_ = proposedScale_;
  currentRotation_ = proposedRotation_;
  currentTranslation_ = proposedTranslation_;
}

void
VariablesHandler::setCurrentIsBest()
{
  bestScale_ = currentScale_;
  bestRotation_ = currentRotation_;
  bestTranslation_ = currentTranslation_;
}

void
VariablesHandler::setBestAsCurrent()
{
  currentScale_ = bestScale_;
  currentRotation_ = bestRotation_;
  currentTranslation_ = bestTranslation_;
}

void
VariablesHandler::getBest(double& scale,
                          RotationMatrix& rotation,
                          TranslationVector& translation) const
{
  scale = bestScale_;
  rotation = bestRotation_;
  translation = bestTranslation_;
}

void
VariablesHandler::setRotationSigma(double sigma)
{
  rotationSigma_ = sigma;
}

void
VariablesHandler::setTranslationSigma(double sigma)
{
  translationSigma_ = sigma;
}

