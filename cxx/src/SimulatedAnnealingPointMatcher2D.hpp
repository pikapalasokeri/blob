#ifndef SimulatedAnnealingPointMatcher2D_hpp
#define SimulatedAnnealingPointMatcher2D_hpp

#include "VariablesHandler.hpp"
#include "Random.hpp"
#include "EigenDefs.hpp"

#include <vector>
#include <utility>
#include <Eigen/Dense>

class SimulatedAnnealingPointMatcher2D
{
public:
  SimulatedAnnealingPointMatcher2D();

  ~SimulatedAnnealingPointMatcher2D();

  void addPoint1(double x, double y);

  void addPoint2(double x, double y);

  void setNumIterations(int);

  void setStartTemperature(double);

  void setInitialRotationSigma(double);

  void setSlowRotationSigma(double);

  void setInitialTranslationSigma(double);

  void setSlowTranslationSigma(double);

  void setSlowMovementBreakpoint(double);

  void setVerbose(bool);

  void setNumThreads(int);

  void match(double* scale, double* rotation, double* translation);

  void output() const;

private:
  void doMatch(double& scaleOut, Eigen::Matrix2d& rotationOut, TranslationVector& translationOut);

  void setUpPointMatrices();

  void transform(const Eigen::MatrixXd& pointMatrix,
                 double scale,
                 const Eigen::Matrix2d& rotation,
                 const TranslationVector& translation,
                 Eigen::MatrixXd& transformedPointMatrix) const;

  double computeFitness(const Eigen::MatrixXd& pointMatrix1,
                        const Eigen::MatrixXd& pointMatrix2) const;

  double computeFitness(double scale, const Eigen::Matrix2d& rotation, const TranslationVector& translation) const;

  using DoublePair = std::pair<double, double>;
  using PointVector = std::vector<DoublePair>;
  PointVector pointSet1_;
  PointVector pointSet2_;
  Eigen::MatrixXd pointMatrix1_;
  Eigen::MatrixXd pointMatrix2_;
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

  MersenneTwister<std::uniform_real_distribution<double> > uniformRandomGenerator_;
};

extern "C" {
  SimulatedAnnealingPointMatcher2D* SimulatedAnnealingPointMatcher2D_new();
  void SimulatedAnnealingPointMatcher2D_delete(SimulatedAnnealingPointMatcher2D*);
  void SimulatedAnnealingPointMatcher2D_addPoint1(SimulatedAnnealingPointMatcher2D*, double x, double y);
  void SimulatedAnnealingPointMatcher2D_addPoint2(SimulatedAnnealingPointMatcher2D*, double x, double y);
  void SimulatedAnnealingPointMatcher2D_setNumIterations(SimulatedAnnealingPointMatcher2D*, int);
  void SimulatedAnnealingPointMatcher2D_setStartTemperature(SimulatedAnnealingPointMatcher2D*, double);
  void SimulatedAnnealingPointMatcher2D_setInitialRotationSigma(SimulatedAnnealingPointMatcher2D*, double);
  void SimulatedAnnealingPointMatcher2D_setSlowRotationSigma(SimulatedAnnealingPointMatcher2D*, double);
  void SimulatedAnnealingPointMatcher2D_setInitialTranslationSigma(SimulatedAnnealingPointMatcher2D*, double);
  void SimulatedAnnealingPointMatcher2D_setSlowTranslationSigma(SimulatedAnnealingPointMatcher2D*, double);
  void SimulatedAnnealingPointMatcher2D_setSlowMovementBreakpoint(SimulatedAnnealingPointMatcher2D*, double);
  void SimulatedAnnealingPointMatcher2D_setVerbose(SimulatedAnnealingPointMatcher2D*, bool);
  void SimulatedAnnealingPointMatcher2D_setNumThreads(SimulatedAnnealingPointMatcher2D*, int);
  void SimulatedAnnealingPointMatcher2D_match(SimulatedAnnealingPointMatcher2D*, double* scale, double* rotation, double* translation);
  void SimulatedAnnealingPointMatcher2D_output(SimulatedAnnealingPointMatcher2D*);
}

#endif
