#ifndef CoherentPointDriftMatcher2D_hpp
#define CoherentPointDriftMatcher2D_hpp

#include "EigenDefs.hpp"

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

  void match(double scale[1][1], double rotation[2][2], double translation[1][2]);

  void output() const;

private:
  void doMatch(double& scaleOut, Eigen::Matrix2d& rotationOut, TranslationVector& translationOut);

  double computeInitialSigmaSquare() const;

  void transform(const Eigen::MatrixXd& pointMatrix,
                 double scale,
                 const Eigen::Matrix2d& rotation,
                 const TranslationVector& translation,
                 Eigen::MatrixXd& transformedPointMatrix) const;

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

#endif
