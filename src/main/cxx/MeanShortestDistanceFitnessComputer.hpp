#ifndef MeanShortestDistanceFitnessComputer_hpp
#define MeanShortestDistanceFitnessComputer_hpp

#include "FitnessComputer.hpp"
#include "EigenDefs.hpp"

class MeanShortestDistanceFitnessComputer : public FitnessComputer
{
public:
  MeanShortestDistanceFitnessComputer(const PointMatrix& referencePoints);

  MeanShortestDistanceFitnessComputer(const double* referencePoints, int dim1, int dim2);

  virtual ~MeanShortestDistanceFitnessComputer() {}

  virtual double compute(const PointMatrix& points) const;

private:
  const PointMatrix referencePoints_;
};

#endif
