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

  virtual double compute(const PointMatrix& points) const;

private:
  const PointMatrix referencePoints_;
  const double tolerance_;
};

#endif
