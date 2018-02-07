%module MeanShortestDistanceFitnessComputer

%{
  #define SWIG_FILE_WITH_INIT
  #include "MeanShortestDistanceFitnessComputer.hpp"
%}

%include "numpy.i"

%init
%{
  import_array();
%}

%apply (double* IN_ARRAY2, int DIM1, int DIM2) {(const double* points, int dim1, int dim2)};

class MeanShortestDistanceFitnessComputer
{
public:
  MeanShortestDistanceFitnessComputer(const double* points, int dim1, int dim2);
};
