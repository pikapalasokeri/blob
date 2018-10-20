#include "SimulatedAnnealingPointMatcher2D.hpp"

#include "FitnessComputer.hpp"
#include "Utilities.hpp"

#include <iostream>

SimulatedAnnealingPointMatcher2D::SimulatedAnnealingPointMatcher2D(
  const FitnessComputer& fitnessComputer)
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
     numThreads_(4),
     fitnessComputer_(fitnessComputer)
{
}

SimulatedAnnealingPointMatcher2D::~SimulatedAnnealingPointMatcher2D()
{
}

void
SimulatedAnnealingPointMatcher2D::addPoint(double x, double y)
{
  pointSet_.emplace_back(x, y);
}


void
SimulatedAnnealingPointMatcher2D::clearPoints()
{
  pointSet_.clear();
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
SimulatedAnnealingPointMatcher2D::match(double scaleOut[1][1], double rotationOut[2][2], double translationOut[1][2], double fitnessOut[1][1])
{
  double scale;
  RotationMatrix rotation;
  TranslationVector translation;
  const double fitness = doMatch(scale, rotation, translation);

  scaleOut[0][0] = scale;
  rotationOut[0][0] = rotation(0, 0);
  rotationOut[0][1] = rotation(0, 1);
  rotationOut[1][0] = rotation(1, 0);
  rotationOut[1][1] = rotation(1, 1);
  translationOut[0][0] = translation(0, 0);
  translationOut[0][1] = translation(0, 1);
  fitnessOut[0][0] = fitness;
}

double
SimulatedAnnealingPointMatcher2D::doMatch(double& scaleOut, RotationMatrix& rotationOut, TranslationVector& translationOut)
{
  setUpPointMatrices();
  variablesHandler_.setRotationSigma(initialRotationSigma_);
  variablesHandler_.setTranslationSigma(initialTranslationSigma_);

  int numGoodMoves = 0;
  int numBadMoves = 0;
  int numNoMoves = 0;

  double oldFitness = fitnessComputer_.compute(pointMatrix_);
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
    RotationMatrix proposedRotation;
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
  return bestFitness;
}

void
SimulatedAnnealingPointMatcher2D::setUpPointMatrices()
{
  const int numPoints = pointSet_.size();

  if (verbose_)
  {
    std::cout << "Num points in set: " << numPoints << std::endl
              << "Num threads: " << numThreads_ << std::endl;
  }

  pointMatrix_ = PointMatrix(numPoints, 2);
  for (int i = 0; i < numPoints; ++i)
  {
    pointMatrix_(i, 0) = pointSet_[i].first;
    pointMatrix_(i, 1) = pointSet_[i].second;
  }
}


double
SimulatedAnnealingPointMatcher2D::computeFitness(double scale, const RotationMatrix& rotation, const TranslationVector& translation) const
{
  PointMatrix transformedPointMatrix;
  Utilities::transform(pointMatrix_, scale, rotation, translation, transformedPointMatrix);

  return fitnessComputer_.compute(transformedPointMatrix);
}

void
SimulatedAnnealingPointMatcher2D::output() const
{
  std::cout << "SimulatedAnnealingPointMatcher2D:" << std::endl;

  std::cout << "  pointSet_:" << std::endl;
  for (auto point : pointSet_)
  {
    std::cout << "    " << point.first << " " << point.second << std::endl;
  }
}
