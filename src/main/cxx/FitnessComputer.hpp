#ifndef FitnessComputer_hpp
#define FitnessComputer_hpp

#include "EigenDefs.hpp"

class FitnessComputer
{
public:
  virtual ~FitnessComputer() {}
  virtual double compute(const PointMatrix& points) const = 0;
};

#endif
