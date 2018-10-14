#ifndef SimulatedAnnealingPointMatcher2D_hpp
#define SimulatedAnnealingPointMatcher2D_hpp

#include "VariablesHandler.hpp"
#include "Random.hpp"
#include "EigenDefs.hpp"

#include <vector>
#include <utility>
#include <Eigen/Dense>

class FitnessComputer;

class SimulatedAnnealingPointMatcher2D
{
public:
  SimulatedAnnealingPointMatcher2D(const FitnessComputer&);

  ~SimulatedAnnealingPointMatcher2D();

  void addPoint1(double x, double y);

  void setNumIterations(int);

  void setStartTemperature(double);

  void setInitialRotationSigma(double);

  void setSlowRotationSigma(double);

  void setInitialTranslationSigma(double);

  void setSlowTranslationSigma(double);

  void setSlowMovementBreakpoint(double);

  void setVerbose(bool);

  void setNumThreads(int);

  void match(double scale[1][1], double rotation[2][2], double translation[1][2], double fitness[1][1]);

  void output() const;

private:
  double doMatch(double& scaleOut, RotationMatrix& rotationOut, TranslationVector& translationOut);

  void setUpPointMatrices();

  void transform(const PointMatrix& pointMatrix,
                 double scale,
                 const RotationMatrix& rotation,
                 const TranslationVector& translation,
                 PointMatrix& transformedPointMatrix) const;

  double computeFitness(double scale, const RotationMatrix& rotation, const TranslationVector& translation) const;

  using DoublePair = std::pair<double, double>;
  using PointVector = std::vector<DoublePair>;
  PointVector pointSet1_;
  PointVector pointSet2_;
  PointMatrix pointMatrix1_;
  int numIterations_;
  double startTemperature_;
  double initialRotationSigma_;
  double slowRotationSigma_;
  double initialTranslationSigma_;
  double slowTranslationSigma_;
  double slowMovementBreakpoint_;
  VariablesHandler variablesHandler_;
  bool verbose_;
  int numThreads_;
  const FitnessComputer& fitnessComputer_;

  MersenneTwister<std::uniform_real_distribution<double> > uniformRandomGenerator_;
};

#endif
