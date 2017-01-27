#ifndef CoherentPointDriftMatcher2D_hpp
#define CoherentPointDriftMatcher2D_hpp

#include <vector>
#include <utility>
#include <Eigen/Dense>

class CoherentPointDriftMatcher2D
{
public:
  CoherentPointDriftMatcher2D();

  ~CoherentPointDriftMatcher2D();

  void addPoint1(double x, double y);

  void addPoint2(double x, double y);

  void setW(double);

  void setMaxIterations(int);

  void setMinIterations(int);

  void setSigmaSquareChangeTolerance(double);

  void setVerbose(bool);
  
  void match(double* scale, double* rotation, double* translation);

  void output() const;

private:
  using TranslationVector = Eigen::Matrix<double, 1, 2>;
  void doMatch(double& scaleOut, Eigen::Matrix2d& rotationOut, TranslationVector& translationOut);

  double computeInitialSigmaSquare() const;

  void transform(const Eigen::MatrixXd& pointMatrix,
                 double scale,
                 const Eigen::Matrix2d& rotation,
                 const TranslationVector& translation,
                 Eigen::MatrixXd& transformedPointMatrix) const;

  double
  solveRigid(const Eigen::MatrixXd& P,
	     double scale,
	     const Eigen::Matrix2d& rotation,
	     const TranslationVector& translation,
	     double& scaleOut,
	     Eigen::Matrix2d& rotationOut,
	     TranslationVector& translationOut) const;
  
  using DoublePair = std::pair<double, double>;
  using PointVector = std::vector<DoublePair>;
  PointVector pointSet1_;
  PointVector pointSet2_;
  Eigen::MatrixXd pointMatrix1_;
  Eigen::MatrixXd pointMatrix2_;
  double w_;
  int maxIterations_;
  int minIterations_;
  double sigmaSquareChangeTolerance_;
  bool verbose_;
  int numThreads_;
};

extern "C" {
  CoherentPointDriftMatcher2D* CoherentPointDriftMatcher2D_new();
  void CoherentPointDriftMatcher2D_delete(CoherentPointDriftMatcher2D*);
  void CoherentPointDriftMatcher2D_addPoint1(CoherentPointDriftMatcher2D*, double x, double y);
  void CoherentPointDriftMatcher2D_addPoint2(CoherentPointDriftMatcher2D*, double x, double y);
  void CoherentPointDriftMatcher2D_setW(CoherentPointDriftMatcher2D*, double);
  void CoherentPointDriftMatcher2D_setMaxIterations(CoherentPointDriftMatcher2D*, int);
  void CoherentPointDriftMatcher2D_setMinIterations(CoherentPointDriftMatcher2D*, int);
  void CoherentPointDriftMatcher2D_setSigmaSquareChangeTolerance(CoherentPointDriftMatcher2D*, double);
  void CoherentPointDriftMatcher2D_setVerbose(CoherentPointDriftMatcher2D*, bool);
  void CoherentPointDriftMatcher2D_match(CoherentPointDriftMatcher2D*, double* scale, double* rotation, double* translation);
  void CoherentPointDriftMatcher2D_output(CoherentPointDriftMatcher2D*);
}

#endif
