#include "BruteForceMatcher.hpp"

#include "FitnessComputer.hpp"
#include <cmath>
#include <cassert>

using namespace Utilities;


namespace
{
  void
  populateCandidates(const double* cloudToMatch,
                     const int numRowsToMatch,
                     const int numColsToMatch,
                     const double minDist,
                     const double maxDist,
                     const int candidateKeepRatio,
                     Utilities::PointVector& candidatePoints1,
                     Utilities::PointVector& candidatePoints2)
  {
    assert(2 == numColsToMatch);
    int candidateCount = 0;
    for (int i = 0; i < numRowsToMatch; ++i)
    {
      const DoublePair point1(cloudToMatch[i * numColsToMatch],
                              cloudToMatch[i * numColsToMatch + 1]);
      for (int j = 0; j < numRowsToMatch; ++j)
      {
        const DoublePair point2(cloudToMatch[j * numColsToMatch],
                                cloudToMatch[j * numColsToMatch + 1]);
        const double diffX = point1.first - point2.first;
        const double diffY = point1.second - point2.second;
        const double distSquare = diffX * diffX + diffY * diffY;
        if (distSquare > minDist && distSquare < maxDist)
        {
          if (0 == (candidateCount++ % candidateKeepRatio))
          {
            candidatePoints1.push_back(point1);
            candidatePoints2.push_back(point2);
          }
        }
      }
    }
  }
}

BruteForceMatcher::BruteForceMatcher(const FitnessComputer& fitnessComputer,
                                     double* pointsReference,
                                     int numRowsReference,
                                     int numColsReference)
  : targetSquareDistance_(0.0),
    targetDistanceTolerance_(0.05),
    fitnessComputer_(fitnessComputer),
    candidateKeepRatio_(1)
{
  assert(2 == numColsReference);
  for (int i1 = 0; i1 < numRowsReference; ++i1)
  {
    const double x1 = pointsReference[i1 * numColsReference];
    const double y1 = pointsReference[i1 * numColsReference + 1];
    for (int i2 = i1 + 1; i2 < numRowsReference; ++i2)
    {
      const double x2 = pointsReference[i2 * numColsReference];
      const double y2 = pointsReference[i2 * numColsReference + 1];
      const double xDiff = x1 - x2;
      const double yDiff = y1 - y2;
      const double squareDistance = xDiff * xDiff + yDiff * yDiff;
      if (squareDistance > targetSquareDistance_)
      {
        targetSquareDistance_ = squareDistance;
        referencePoint1_(0, 0) = x1;
        referencePoint1_(0, 1) = y1;
        referencePoint2_(0, 0) = x2;
        referencePoint2_(0, 1) = y2;
      }
    }
  }
}

void
BruteForceMatcher::setCandidateKeepRatio(const int candidateKeepRatio)
{
  candidateKeepRatio_ = candidateKeepRatio;
}

void BruteForceMatcher::setCandidateDistanceTolerance(const double tolerance)
{
  targetDistanceTolerance_ = tolerance;
}

void
BruteForceMatcher::match(double* cloudToMatch,
                         int numRowsToMatch,
                         int numColsToMatch,
                         double scaleOut[1][1],
                         double rotationOut[2][2],
                         double translationOut[1][2],
                         double fitnessOut[1][1])
{
  double scale;
  RotationMatrix rotation;
  TranslationVector translation;
  const double fitness = doMatch(cloudToMatch,
                                 numRowsToMatch,
                                 numColsToMatch,
                                 scale,
                                 rotation,
                                 translation);

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
BruteForceMatcher::doMatch(const double* cloudToMatch,
                           const int numRowsToMatch,
                           const int numColsToMatch,
                           double& scaleOut,
                           RotationMatrix& rotationOut,
                           TranslationVector& translationOut) const
{
  const double minSqDist = targetSquareDistance_ * (1.0 - targetDistanceTolerance_);
  const double maxSqDist = targetSquareDistance_ * (1.0 + targetDistanceTolerance_);
  Utilities::PointVector candidatePoints1;
  Utilities::PointVector candidatePoints2;
  populateCandidates(cloudToMatch,
                     numRowsToMatch,
                     numColsToMatch,
                     minSqDist,
                     maxSqDist,
                     candidateKeepRatio_,
                     candidatePoints1,
                     candidatePoints2);

  const PointMatrix cloudToMatchMatrix(Utilities::toPointMatrix(cloudToMatch,
                                                                numRowsToMatch,
                                                                numColsToMatch));
  double bestFitness = std::numeric_limits<double>::max();
  RotationMatrix bestRotation;
  TranslationVector bestTranslation;
  const double scale = 1.0;

  PointVector::const_iterator it1 = candidatePoints1.begin();
  PointVector::const_iterator it2 = candidatePoints2.begin();
  PointVector::const_iterator end1 = candidatePoints1.end();
  for (; it1 != end1; ++it1, ++it2)
  {
    RotationMatrix rotation;
    TranslationVector translation;
    computeTransformation(*it1, *it2, rotation, translation);

    PointMatrix transformedPointMatrix;
    Utilities::transform(cloudToMatchMatrix, scale, rotation, translation, transformedPointMatrix);
    const double fitness = fitnessComputer_.compute(transformedPointMatrix);
    if (fitness < bestFitness)
    {
      bestFitness = fitness;
      bestRotation = rotation;
      bestTranslation = translation;
    }
  }

  scaleOut = scale;
  rotationOut = bestRotation;
  translationOut = bestTranslation;
  return bestFitness;
}

void
BruteForceMatcher::computeTransformation(const DoublePair& p1tmp,
                                         const DoublePair& p2tmp,
                                         RotationMatrix& rotationOut,
                                         TranslationVector& translationOut) const
{
  const EigVector p1(p1tmp.first, p1tmp.second);
  const EigVector p2(p2tmp.first, p2tmp.second);

  const EigVector targetVector = referencePoint1_ - referencePoint2_;
  const EigVector targetPoint = referencePoint1_;
  const EigVector candidateVector = p1 - p2;
  const EigVector candidatePoint = p1;

  const double cos = targetVector.dot(candidateVector)/(targetVector.norm() * candidateVector.norm());
  double alpha = std::acos(cos);
  const double crossProduct = targetVector(0, 0) * candidateVector(0, 1)
                              - targetVector(0, 1) * candidateVector(0, 0);
  if (crossProduct > 0.0)
  {
    alpha = -alpha;
  }
  const double c = std::cos(alpha);
  const double s = std::sin(alpha);
  rotationOut(0, 0) = c;
  rotationOut(0, 1) = -s;
  rotationOut(1, 0) = s;
  rotationOut(1, 1) = c;
  translationOut = targetPoint - candidatePoint * rotationOut.transpose();
}
