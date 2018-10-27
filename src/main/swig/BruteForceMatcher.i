%module BruteForceMatcher

%{
#define SWIG_FILE_WITH_INIT
#include "BruteForceMatcher.hpp"
%}

%include "numpy.i"

%init
%{
  import_array();
%}

%apply (double* IN_ARRAY2, int DIM1, int DIM2) {(double* points, int dim1, int dim2)};
%apply (double ARGOUT_ARRAY2[ANY][ANY]) {(double scale[1][1])};
%apply (double ARGOUT_ARRAY2[ANY][ANY]) {(double rotation[2][2])};
%apply (double ARGOUT_ARRAY2[ANY][ANY]) {(double translation[1][2])};
%apply (double ARGOUT_ARRAY2[ANY][ANY]) {(double fitness[1][1])};

class BruteForceMatcher
{
public:
  BruteForceMatcher(const FitnessComputer&,
                    double* points,
                    int dim1,
                    int dim2);

  void setCandidateKeepRatio(const int candidateKeepRatio);

  void setCandidateDistanceTolerance(const double tolerance);

  void match(double* points,
             int dim1,
             int dim2,
             double scale[1][1],
             double rotation[2][2],
             double translation[1][2],
             double fitness[1][1]);
};
