#include "AbsoluteNeighborFitnessComputer.hpp"

#include "Utilities.hpp"
#include <utility>

using namespace std;

AbsoluteNeighborFitnessComputer::AbsoluteNeighborFitnessComputer(
  const PointMatrix& referencePoints,
  double tolerance)
  : referencePoints_(referencePoints),
    tolerance_(tolerance)
{}

AbsoluteNeighborFitnessComputer::AbsoluteNeighborFitnessComputer(
  const double* referencePoints,
  int dim1,
  int dim2,
  double tolerance)
  : referencePoints_(Utilities::toPointMatrix(referencePoints, dim1, dim2)),
    tolerance_(tolerance)
{}

double
AbsoluteNeighborFitnessComputer::compute(const double* points,
                                         int dim1,
                                         int dim2) const
{
  return compute(Utilities::toPointMatrix(points, dim1, dim2));
}

double
AbsoluteNeighborFitnessComputer::compute(const PointMatrix& points) const
{
  const int numRefRows = referencePoints_.rows();
  if (tolerance_ <= 0.0 ||
      numRefRows == 0)
    return 1.0;

  const int numCols = referencePoints_.cols();
  const int numCheckRows = points.rows();

  assert(numCols == points.cols());

  const double toleranceSquare_ = tolerance_ * tolerance_;
  int numWithinTolerance = 0;
  for (int iRef = 0; iRef < numRefRows; ++iRef)
  {
    const double xRef = referencePoints_(iRef, 0);
    const double yRef = referencePoints_(iRef, 1);
    bool foundReference = false;
    for (int iCheck = 0; iCheck < numCheckRows; ++iCheck)
    {
      const double diffX = xRef - points(iCheck, 0);
      const double diffY = yRef - points(iCheck, 1);
      const double squareDistance = diffX*diffX + diffY*diffY;
      if (squareDistance <= toleranceSquare_)
      {
        foundReference = true;
        break;
      }
    }

    if (foundReference)
    {
      ++numWithinTolerance;
    }
  }

  return double(numRefRows - numWithinTolerance) / numRefRows;
}
