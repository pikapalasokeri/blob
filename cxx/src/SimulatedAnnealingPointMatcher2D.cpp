#include "SimulatedAnnealingPointMatcher2D.hpp"

#include "Utilities.hpp"

#include <iostream>

SimulatedAnnealingPointMatcher2D::SimulatedAnnealingPointMatcher2D()
  :  numIterations_(200),
     startTemperature_(10.0),
     initialRotationSigma_(90.0),
     slowRotationSigma_(2.0),
     initialTranslationSigma_(3.0),
     slowTranslationSigma_(1.0),
     slowMovementBreakpoint_(0.75),
     variablesHandler_(initialRotationSigma_,
                       initialTranslationSigma_),
     verbose_(false),
     numThreads_(4)
{
}

SimulatedAnnealingPointMatcher2D::~SimulatedAnnealingPointMatcher2D()
{
}

void
SimulatedAnnealingPointMatcher2D::addPoint1(double x, double y)
{
  pointSet1_.emplace_back(x, y);
}

void
SimulatedAnnealingPointMatcher2D::addPoint2(double x, double y)
{
  pointSet2_.emplace_back(x, y);
}

void
SimulatedAnnealingPointMatcher2D::setNumIterations(int numIterations)
{
  numIterations_ = numIterations;
}

void
SimulatedAnnealingPointMatcher2D::setStartTemperature(double temperature)
{
  startTemperature_ = temperature;
}

void
SimulatedAnnealingPointMatcher2D::setInitialRotationSigma(double sigma)
{
  initialRotationSigma_ = sigma;
}

void
SimulatedAnnealingPointMatcher2D::setSlowRotationSigma(double sigma)
{
  slowRotationSigma_ = sigma;
}

void
SimulatedAnnealingPointMatcher2D::setInitialTranslationSigma(double sigma)
{
  initialTranslationSigma_ = sigma;
}

void
SimulatedAnnealingPointMatcher2D::setSlowTranslationSigma(double sigma)
{
  slowTranslationSigma_ = sigma;
}

void
SimulatedAnnealingPointMatcher2D::setSlowMovementBreakpoint(double breakpoint)
{
  slowMovementBreakpoint_ = breakpoint;
}

void
SimulatedAnnealingPointMatcher2D::setVerbose(bool verbose)
{
  verbose_ = verbose;
}

void
SimulatedAnnealingPointMatcher2D::setNumThreads(int numThreads)
{
  numThreads_ = numThreads;
}

void
SimulatedAnnealingPointMatcher2D::match(double* scaleOut, double* rotationOut, double* translationOut)
{
  double scale;
  Eigen::Matrix2d rotation;
  TranslationVector translation;
  doMatch(scale, rotation, translation);

  scaleOut[0] = scale;
  rotationOut[0] = rotation(0, 0);
  rotationOut[1] = rotation(0, 1);
  rotationOut[2] = rotation(1, 0);
  rotationOut[3] = rotation(1, 1);
  translationOut[0] = translation(0, 0);
  translationOut[1] = translation(0, 1);
}

void
SimulatedAnnealingPointMatcher2D::doMatch(double& scaleOut, Eigen::Matrix2d& rotationOut, TranslationVector& translationOut)
{
  setUpPointMatrices();
  variablesHandler_.setRotationSigma(initialRotationSigma_);
  variablesHandler_.setTranslationSigma(initialTranslationSigma_);

  int numGoodMoves = 0;
  int numBadMoves = 0;
  int numNoMoves = 0;

  double oldFitness = computeFitness(pointMatrix1_, pointMatrix2_);
  double bestFitness = oldFitness;
  for (int i = 0; i < numIterations_; ++i)
  {
    if (i == int(numIterations_ * slowMovementBreakpoint_))
    {
      variablesHandler_.setRotationSigma(slowRotationSigma_);
      variablesHandler_.setTranslationSigma(slowTranslationSigma_);
      variablesHandler_.setBestAsCurrent();
    }

    double proposedScale;
    Eigen::Matrix2d proposedRotation;
    TranslationVector proposedTranslation;
    variablesHandler_.proposeNewVariables(proposedScale, proposedRotation, proposedTranslation);
    const double newFitness = computeFitness(proposedScale, proposedRotation, proposedTranslation);

    const double deltaFitness = newFitness - oldFitness;
    if (deltaFitness < 0.0)
    {
      ++numGoodMoves;
      variablesHandler_.acceptProposed();
    }
    else
    {
      const double randomNumber = uniformRandomGenerator_.getNext();
      const double temperature = double(numIterations_ - i) / numIterations_ * startTemperature_;
      const double boltzmannFactor = exp(-deltaFitness/temperature);
      if (boltzmannFactor > randomNumber)
      {
        ++numBadMoves;
        variablesHandler_.acceptProposed();
      }
      else
      {
        ++numNoMoves;
      }
    }

    if (newFitness < bestFitness)
    {
      bestFitness = newFitness;
      variablesHandler_.setCurrentIsBest();
      if (verbose_)
      {
        std::cout << "New best. Fitness: " << bestFitness << std::endl;
      }
    }

    oldFitness = newFitness;
  }

  if (verbose_)
  {
    std::cout << "Annealing complete." << std::endl
              << "Fitness: " << bestFitness << std::endl
              << "Num good moves: " << numGoodMoves << std::endl
              << "Num bad moves: " << numBadMoves << std::endl
              << "Num no moves: " << numNoMoves << std::endl;
  }

  variablesHandler_.getBest(scaleOut, rotationOut, translationOut);
}

void
SimulatedAnnealingPointMatcher2D::setUpPointMatrices()
{
  const int num1Points = pointSet1_.size();
  const int num2Points = pointSet2_.size();

  if (verbose_)
  {
    std::cout << "Num points in set 1: " << num1Points << std::endl
              << "Num points in set 2: " << num2Points << std::endl
              << "Num threads: " << numThreads_ << std::endl;
  }

  pointMatrix1_ = Eigen::MatrixXd(num1Points, 2);
  for (int i = 0; i < num1Points; ++i)
  {
    pointMatrix1_(i, 0) = pointSet1_[i].first;
    pointMatrix1_(i, 1) = pointSet1_[i].second;
  }

  pointMatrix2_ = Eigen::MatrixXd(num2Points, 2);
  for (int i = 0; i < num2Points; ++i)
  {
    pointMatrix2_(i, 0) = pointSet2_[i].first;
    pointMatrix2_(i, 1) = pointSet2_[i].second;
  }
}

namespace
{
  double
  mean(const std::vector<double> v1)
  {
    if (v1.size() == 0)
    {
      return 0.0;
    }

    double sum = 0.0;
    for (double value : v1)
    {
      sum += value;
    }

    return sum / v1.size();
  }
}

double
SimulatedAnnealingPointMatcher2D::computeFitness(const Eigen::MatrixXd& pointMatrix1,
                                                 const Eigen::MatrixXd& pointMatrix2) const
{
  assert(pointMatrix2.cols() == 2);
  const int numRows1 = pointMatrix1.rows();
  const int numRows2 = pointMatrix2.rows();
  std::vector<double> shortestFrom1(numRows1, 1.0e10);
  std::vector<double> shortestFrom2(numRows2, 1.0e10);

  for (int rowIx1 = 0; rowIx1 < numRows1; ++rowIx1)
  {
    for (int rowIx2 = 0; rowIx2 < numRows2; ++rowIx2)
    {
      const double diffX = pointMatrix1(rowIx1, 0) - pointMatrix2(rowIx2, 0);
      const double diffY = pointMatrix1(rowIx1, 1) - pointMatrix2(rowIx2, 1);
      const double squareDistance = diffX * diffX + diffY * diffY;

      if (squareDistance < shortestFrom1[rowIx1])
      {
        shortestFrom1[rowIx1] = squareDistance;
      }
      if (squareDistance < shortestFrom2[rowIx2])
      {
        shortestFrom2[rowIx2] = squareDistance;
      }
    }
  }

  return mean(shortestFrom1) + mean(shortestFrom2);
}

double
SimulatedAnnealingPointMatcher2D::computeFitness(double scale, const Eigen::Matrix2d& rotation, const TranslationVector& translation) const
{
  Eigen::MatrixXd transformedPointMatrix1;
  Utilities::transform(pointMatrix1_, scale, rotation, translation, transformedPointMatrix1);

  return computeFitness(transformedPointMatrix1, pointMatrix2_);
}

void
SimulatedAnnealingPointMatcher2D::output() const
{
  std::cout << "SimulatedAnnealingPointMatcher2D:" << std::endl;

  std::cout << "  pointSet1_:" << std::endl;
  for (auto point : pointSet1_)
  {
    std::cout << "    " << point.first << " " << point.second << std::endl;
  }

  std::cout << "  pointSet2_:" << std::endl;
  for (auto point : pointSet2_)
  {
    std::cout << "    " << point.first << " " << point.second << std::endl;
  }
}

extern "C" {
  SimulatedAnnealingPointMatcher2D* SimulatedAnnealingPointMatcher2D_new()
  {
    return new SimulatedAnnealingPointMatcher2D();
  }

  void SimulatedAnnealingPointMatcher2D_delete(SimulatedAnnealingPointMatcher2D* matcher)
  {
    delete matcher;
  }

  void SimulatedAnnealingPointMatcher2D_addPoint1(SimulatedAnnealingPointMatcher2D* matcher, double x, double y)
  {
    matcher->addPoint1(x,y);
  }

  void SimulatedAnnealingPointMatcher2D_addPoint2(SimulatedAnnealingPointMatcher2D* matcher, double x, double y)
  {
    matcher->addPoint2(x,y);
  }

  void SimulatedAnnealingPointMatcher2D_setNumIterations(SimulatedAnnealingPointMatcher2D* matcher, int numIterations)
  {
    matcher->setNumIterations(numIterations);
  }

  void SimulatedAnnealingPointMatcher2D_setStartTemperature(SimulatedAnnealingPointMatcher2D* matcher, double temperature)
  {
    matcher->setStartTemperature(temperature);
  }

  void SimulatedAnnealingPointMatcher2D_setInitialRotationSigma(SimulatedAnnealingPointMatcher2D* matcher, double sigma)
  {
    matcher->setInitialRotationSigma(sigma);
  }

  void SimulatedAnnealingPointMatcher2D_setSlowRotationSigma(SimulatedAnnealingPointMatcher2D* matcher, double sigma)
  {
    matcher->setSlowRotationSigma(sigma);
  }

  void SimulatedAnnealingPointMatcher2D_setInitialTranslationSigma(SimulatedAnnealingPointMatcher2D* matcher, double sigma)
  {
    matcher->setInitialTranslationSigma(sigma);
  }

  void SimulatedAnnealingPointMatcher2D_setSlowTranslationSigma(SimulatedAnnealingPointMatcher2D* matcher, double sigma)
  {
    matcher->setSlowTranslationSigma(sigma);
  }

  void SimulatedAnnealingPointMatcher2D_setSlowMovementBreakpoint(SimulatedAnnealingPointMatcher2D* matcher, double breakpoint)
  {
    matcher->setSlowMovementBreakpoint(breakpoint);
  }

  void SimulatedAnnealingPointMatcher2D_setVerbose(SimulatedAnnealingPointMatcher2D* matcher, bool verbose)
  {
    matcher->setVerbose(verbose);
  }

  void SimulatedAnnealingPointMatcher2D_setNumThreads(SimulatedAnnealingPointMatcher2D* matcher, int numThreads)
  {
    matcher->setNumThreads(numThreads);
  }

  void SimulatedAnnealingPointMatcher2D_match(SimulatedAnnealingPointMatcher2D* matcher, double* scale, double* rotation, double* translation)
  {
    matcher->match(scale, rotation, translation);
  }

  void SimulatedAnnealingPointMatcher2D_output(SimulatedAnnealingPointMatcher2D* matcher)
  {
    matcher->output();
  }
}
