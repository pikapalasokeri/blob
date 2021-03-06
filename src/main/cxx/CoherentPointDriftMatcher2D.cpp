#include "CoherentPointDriftMatcher2D.hpp"

#include "RigidSolver.hpp"
#include "Utilities.hpp"

#include <Eigen/Dense>
#include <Eigen/SVD>
#include <iostream>
#include <cmath>
#include <time.h>
#include <omp.h>

CoherentPointDriftMatcher2D::CoherentPointDriftMatcher2D()
  : w_(0.0),
    maxIterations_(100),
    minIterations_(50),
    sigmaSquareChangeTolerance_(0.001),
    verbose_(false),
    numThreads_(4)
{
}

CoherentPointDriftMatcher2D::~CoherentPointDriftMatcher2D()
{
}

void
CoherentPointDriftMatcher2D::addPoint1(double x, double y)
{
  pointSet1_.emplace_back(x, y);
}

void
CoherentPointDriftMatcher2D::addPoint2(double x, double y)
{
  pointSet2_.emplace_back(x, y);
}

void
CoherentPointDriftMatcher2D::setW(double w)
{
  w_ = w;
}

void
CoherentPointDriftMatcher2D::setMaxIterations(int maxIterations)
{
  maxIterations_ = maxIterations;
}

void
CoherentPointDriftMatcher2D::setMinIterations(int minIterations)
{
  minIterations_ = minIterations;
}

void
CoherentPointDriftMatcher2D::setSigmaSquareChangeTolerance(double sigmaSquareChangeTolerance)
{
  sigmaSquareChangeTolerance_ = sigmaSquareChangeTolerance;
}

void
CoherentPointDriftMatcher2D::setVerbose(bool verbose)
{
  verbose_ = verbose;
}

void
CoherentPointDriftMatcher2D::match(double scaleOut[1][1],
                                   double rotationOut[2][2],
                                   double translationOut[1][2])
{
  double scale;
  Eigen::Matrix2d rotation;
  TranslationVector translation;
  doMatch(scale, rotation, translation);
  scaleOut[0][0] = scale;
  rotationOut[0][0] = rotation(0, 0);
  rotationOut[0][1] = rotation(0, 1);
  rotationOut[1][0] = rotation(1, 0);
  rotationOut[1][1] = rotation(1, 1);
  translationOut[0][0] = translation(0, 0);
  translationOut[0][1] = translation(0, 1);
}

void
CoherentPointDriftMatcher2D::doMatch(double& scaleOut, Eigen::Matrix2d& rotationOut, TranslationVector& translationOut)
{
  const double pi = acos(-1.0);

  double scale = 1.0;
  Eigen::Matrix2d rotation;
  rotation << 1.0, 0.0,
              0.0, 1.0;
  TranslationVector translation;
  translation << 0.0, 0.0;

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

  double sigmaSquare = computeInitialSigmaSquare();

  Eigen::MatrixXd P = Eigen::MatrixXd::Constant(num1Points, num2Points, 0.0);

  std::vector<Eigen::MatrixXd> tiledJPoints;
  tiledJPoints.reserve(num2Points);
  for (int i = 0; i < num2Points; ++i)
  {
    Eigen::MatrixXd tiledPoint = Eigen::MatrixXd::Constant(num1Points, 2, 0.0);
    tiledPoint.col(0) = pointMatrix2_(i, 0) * Eigen::MatrixXd::Ones(num1Points, 1);
    tiledPoint.col(1) = pointMatrix2_(i, 1) * Eigen::MatrixXd::Ones(num1Points, 1);
    tiledJPoints.push_back(tiledPoint);
  }

  Eigen::MatrixXd numerators(num1Points, num2Points);
  Eigen::MatrixXd denominators(num1Points, num2Points);

  double oldSigmaSquare = 1.0e+10;
  int ix = 0;
  while (true)
  {
    const double sigmaSquareChange = fabs(oldSigmaSquare - sigmaSquare);
    oldSigmaSquare = sigmaSquare;

    if (verbose_)
    {
      std::cout << "Iteration: " << ix << std::endl
                << "  sigmaSquare: " << sigmaSquare << std::endl
                << "  Change in sigmaSquare: " << sigmaSquareChange << std::endl
                << "  scale: " << scale << std::endl
                << "  rotation: " << std::endl << rotation << std::endl
                << "  translation: " << translation << std::endl;
    }

    if (ix >= maxIterations_ ||
        sigmaSquare <= 0.0 ||
        (ix > minIterations_ && sigmaSquareChange < sigmaSquareChangeTolerance_))
    {
      break;
    }
    ++ix;

    Eigen::MatrixXd transformedPointMatrix1(num1Points, 2);
    Utilities::transform(pointMatrix1_, scale, rotation, translation, transformedPointMatrix1);

    const double constant1 = -1.0/(2.0*sigmaSquare);
    const double constant2 = 2.0 * pi * sigmaSquare * w_ / (1.0 - w_) * double(num1Points)/double(num2Points);

#pragma omp parallel for num_threads(numThreads_)
    for (int j = 0; j < num2Points; ++j)
    {
      const Eigen::MatrixXd exponents = constant1 * (tiledJPoints[j] - transformedPointMatrix1).rowwise().squaredNorm();

      double denominatorSum = 0.0;
      for (int i = 0; i < num1Points; ++i)
      {
        const Eigen::Matrix<double, 1, 2> sjTmiDiff = pointMatrix2_.block(j, 0, 1, 2) - transformedPointMatrix1.block(i, 0, 1, 2);
        const double dotProduct = sjTmiDiff.dot(sjTmiDiff);
        numerators(i, j) = std::exp(constant1 * dotProduct);

        denominatorSum += std::exp(exponents(i, 0));
      }
      denominators.block(0, j, num1Points, 1) = (denominatorSum + constant2) * Eigen::MatrixXd::Ones(num1Points, 1);
    }

    P = numerators.array() / denominators.array();

    RigidSolver rigidSolver(pointMatrix1_, pointMatrix2_, P);
    sigmaSquare = rigidSolver.solve(scaleOut, rotationOut, translationOut);

    scale = scaleOut;
    rotation = rotationOut;
    translation = translationOut;
  }
}

double
CoherentPointDriftMatcher2D::computeInitialSigmaSquare() const
{
  double sum = 0.0;
  for (const auto& point1 : pointSet1_)
  {
    for (const auto& point2 : pointSet2_)
    {
      const DoublePair diff(point1.first - point2.first, point1.second - point2.second);
      sum += diff.first*diff.first + diff.second*diff.second;
    }
  }
  return sum/(2.0 * pointSet1_.size() * pointSet2_.size());
}

void
CoherentPointDriftMatcher2D::output() const
{
  std::cout << "CoherentPointDriftMatcher2D:" << std::endl;

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
