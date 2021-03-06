%module SimulatedAnnealingPointMatcher2D

%{
  #define SWIG_FILE_WITH_INIT
  #include "SimulatedAnnealingPointMatcher2D.hpp"
  #include "FitnessComputer.hpp"
%}

%include "numpy.i"
%include "FitnessComputer.hpp"

%init
%{
  import_array();
%}

%apply (double ARGOUT_ARRAY2[ANY][ANY]) {(double scale[1][1])};
%apply (double ARGOUT_ARRAY2[ANY][ANY]) {(double rotation[2][2])};
%apply (double ARGOUT_ARRAY2[ANY][ANY]) {(double translation[1][2])};
%apply (double ARGOUT_ARRAY2[ANY][ANY]) {(double fitness[1][1])};

class SimulatedAnnealingPointMatcher2D
{
public:
  SimulatedAnnealingPointMatcher2D(const FitnessComputer&);

  ~SimulatedAnnealingPointMatcher2D();

  void addPoint(double x, double y);

  void clearPoints();

  void setNumIterations(int);

  void setStartTemperature(double);

  void setInitialRotationSigma(double);

  void setSlowRotationSigma(double);

  void setInitialTranslationSigma(double);

  void setSlowTranslationSigma(double);

  void setSlowMovementBreakpoint(double);

  void setVerbose(bool);

  void setNumThreads(int);

  void match(double scale[1][1], double rotation[2][2], double translation[1][2], double fitness[1][1]);

  void output() const;
};
