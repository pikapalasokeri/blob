#include "AbsoluteNeighborFitnessComputer.hpp"

#include "Utilities.hpp"
#include <utility>

using namespace std;

AbsoluteNeighborFitnessComputer::AbsoluteNeighborFitnessComputer(
  const PointMatrix& referencePoints,
  double tolerance)
  : referencePoints_(referencePoints),
    tolerance_(tolerance),
    toleranceSquare_(tolerance_ * tolerance_)
{}

AbsoluteNeighborFitnessComputer::AbsoluteNeighborFitnessComputer(
  const double* referencePoints,
  int dim1,
  int dim2,
  double tolerance)
  : referencePoints_(Utilities::toPointMatrix(referencePoints, dim1, dim2)),
    tolerance_(tolerance),
    toleranceSquare_(tolerance_ * tolerance_)
{}

double
AbsoluteNeighborFitnessComputer::compute(const double* points,
                                         int dim1,
                                         int dim2) const
{
  return compute(Utilities::toPointMatrix(points, dim1, dim2));
}

bool
AbsoluteNeighborFitnessComputer::lookForMatchInRange(const PointMatrix& points,
                                                     const double xRef,
                                                     const double yRef,
                                                     const int fromIx,
                                                     const int toIx,
                                                     int& matchIxOut) const
{
  for (int iCheck = fromIx; iCheck < toIx; ++iCheck)
  {
    const double diffX = xRef - points(iCheck, 0);
    const double diffY = yRef - points(iCheck, 1);

    const double squareDistance = diffX*diffX + diffY*diffY;
    if (squareDistance <= toleranceSquare_)
    {
      matchIxOut = iCheck;
      return true;
    }
  }
  return false;
}

double
AbsoluteNeighborFitnessComputer::compute(const PointMatrix& points) const
{
  const int numRefRows = referencePoints_.rows();
  if (tolerance_ <= 0.0 ||
      numRefRows == 0 ||
      points.rows() == 0)
    return 1.0;

  const int numCols = referencePoints_.cols();
  const int numCheckRows = points.rows();

  assert(numCols == points.cols());

  PointMatrix pointsMax(points.colwise().maxCoeff());
  PointMatrix pointsMin(points.colwise().minCoeff());

  int matchIx = 0;
  int numWithinTolerance = 0;
  for (int iRef = 0; iRef < numRefRows; ++iRef)
  {
    const double xRef = referencePoints_(iRef, 0);
    const double yRef = referencePoints_(iRef, 1);

    const int fromIx = std::max(matchIx - 10, 0);
    bool foundReference = lookForMatchInRange(points,
                                              xRef,
                                              yRef,
                                              fromIx,
                                              numCheckRows,
                                              matchIx);
    if (foundReference)
    {
      ++numWithinTolerance;
    }
    else
    {
      foundReference = lookForMatchInRange(points,
                                           xRef,
                                           yRef,
                                           0,
                                           fromIx,
                                           matchIx);
      if (foundReference)
      {
        ++numWithinTolerance;
      }
    }
  }

  return double(numRefRows - numWithinTolerance) / numRefRows;
}
