%module MostPopulatedCircleFinder

%{
  #define SWIG_FILE_WITH_INIT
  #include "MostPopulatedCircleFinder.hpp"
%}

%include "numpy.i"

%init
%{
  import_array();
%}

%typemap(out) Point
%{
  $result = PyTuple_Pack(2, PyFloat_FromDouble($1.first), PyFloat_FromDouble($1.second));
%}

%apply (double* IN_ARRAY2, int DIM1, int DIM2) {(double* points, int dim1, int dim2)};

class MostPopulatedCircleFinder
{
public:
  MostPopulatedCircleFinder(double* points, int dim1, int dim2);

  Point get(double radius) const;
};
