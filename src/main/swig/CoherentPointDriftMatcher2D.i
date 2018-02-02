%module CoherentPointDriftMatcher2D

%{
  #define SWIG_FILE_WITH_INIT
  #include "CoherentPointDriftMatcher2D.hpp"
%}

%include "numpy.i"

%init
%{
  import_array();
%}

%apply (double ARGOUT_ARRAY2[ANY][ANY]) {(double scale[1][1])};
%apply (double ARGOUT_ARRAY2[ANY][ANY]) {(double rotation[2][2])};
%apply (double ARGOUT_ARRAY2[ANY][ANY]) {(double translation[1][2])};

class CoherentPointDriftMatcher2D
{
public:
  CoherentPointDriftMatcher2D();

  void addPoint1(double x, double y);

  void addPoint2(double x, double y);

  void setW(double);

  void setMaxIterations(int);

  void setMinIterations(int);

  void setSigmaSquareChangeTolerance(double);

  void setVerbose(bool);

  void match(double scale[1][1], double rotation[2][2], double translation[1][2]);

  void output() const;
};
