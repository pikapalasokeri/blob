%module SimulatedAnnealingPointMatcher2D

%{
  #define SWIG_FILE_WITH_INIT
  #include "SimulatedAnnealingPointMatcher2D.hpp"
%}

%include "numpy.i"

%init
%{
  import_array();
%}

%apply (double ARGOUT_ARRAY2[ANY][ANY]) {(double scale[1][1])};
%apply (double ARGOUT_ARRAY2[ANY][ANY]) {(double rotation[2][2])};
%apply (double ARGOUT_ARRAY2[ANY][ANY]) {(double translation[1][2])};

class SimulatedAnnealingPointMatcher2D
{
public:
  SimulatedAnnealingPointMatcher2D();

  ~SimulatedAnnealingPointMatcher2D();

  void addPoint1(double x, double y);

  void addPoint2(double x, double y);

  void setNumIterations(int);

  void setStartTemperature(double);

  void setInitialRotationSigma(double);

  void setSlowRotationSigma(double);

  void setInitialTranslationSigma(double);

  void setSlowTranslationSigma(double);

  void setSlowMovementBreakpoint(double);

  void setVerbose(bool);

  void setNumThreads(int);

  void match(double scale[1][1], double rotation[2][2], double translation[1][2]);

  void output() const;
};
