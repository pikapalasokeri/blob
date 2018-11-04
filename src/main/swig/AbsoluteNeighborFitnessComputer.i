%module AbsoluteNeighborFitnessComputer

%{
#define SWIG_FILE_WITH_INIT
#include "AbsoluteNeighborFitnessComputer.hpp"
%}

%include "numpy.i"
%include "FitnessComputer.hpp"

%init
%{
  import_array();
%}

%apply (double* IN_ARRAY2, int DIM1, int DIM2) {(const double* points, int dim1, int dim2)};
%feature ("notabstract") AbsoluteNeighborFitnessComputer;

class AbsoluteNeighborFitnessComputer : public FitnessComputer
{
public:
  AbsoluteNeighborFitnessComputer(const double* points, int dim1, int dim2, double tolerance);
  virtual ~AbsoluteNeighborFitnessComputer();
  double compute(const double* points, int dim1, int dim2);
};

