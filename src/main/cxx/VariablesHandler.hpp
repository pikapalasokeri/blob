#ifndef VariablesHandler_hpp
#define VariablesHandler_hpp

#include "Random.hpp"
#include "EigenDefs.hpp"
#include <Eigen/Dense>
#include <random>

class VariablesHandler
{
public:
  VariablesHandler(double rotationSigma,
                   double translationSigma);

  void proposeNewVariables(double& scale,
                           RotationMatrix& rotation,
                           TranslationVector& translation);

  void acceptProposed();

  void setCurrentIsBest();

  void setBestAsCurrent();

  void getBest(double& scale,
               RotationMatrix& rotation,
               TranslationVector& translation) const;

  void setRotationSigma(double);

  void setTranslationSigma(double);

private:
  double rotationSigma_;
  double translationSigma_;

  double currentScale_;
  RotationMatrix currentRotation_;
  TranslationVector currentTranslation_;

  double proposedScale_;
  RotationMatrix proposedRotation_;
  TranslationVector proposedTranslation_;

  double bestScale_;
  RotationMatrix bestRotation_;
  TranslationVector bestTranslation_;

  const double pi_;

  MersenneTwister<std::normal_distribution<double> > normalRandomGenerator_;
};

#endif
