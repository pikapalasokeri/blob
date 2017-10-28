#ifndef MeanShortestDistanceFitnessComputer_hpp
#define MeanShortestDistanceFitnessComputer_hpp

#include "EigenDefs.hpp"

class MeanShortestDistanceFitnessComputer
{
public:
  double compute(const PointMatrix& points1, const PointMatrix& points2) const;
};

#endif
