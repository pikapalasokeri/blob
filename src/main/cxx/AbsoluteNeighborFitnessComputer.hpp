#ifndef AbsoluteNeighborFitnessComputer_hpp
#define AbsoluteNeighborFitnessComputer_hpp

#include "FitnessComputer.hpp"
#include "EigenDefs.hpp"

class AbsoluteNeighborFitnessComputer : public FitnessComputer
{
public:
  AbsoluteNeighborFitnessComputer(const PointMatrix& referencePoints, double tolerance);

  AbsoluteNeighborFitnessComputer(const double* referencePoints, int dim1, int dim2, double tolerance);

  virtual ~AbsoluteNeighborFitnessComputer() {}
  double compute(const double* points, int dim1, int dim2) const;
  virtual double compute(const PointMatrix& points) const;

private:
  bool lookForMatchInRange(const PointMatrix& points,
                           const double xRef,
                           const double yRef,
                           const int fromIx,
                           const int toIx,
                           int& matchIxOut) const;

  const PointMatrix referencePoints_;
  const double tolerance_;
  const double toleranceSquare_;
};

#endif
