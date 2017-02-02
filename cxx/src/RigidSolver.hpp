#include "EigenDefs.hpp"
#include <Eigen/Dense>

class RigidSolver
{
public:
  RigidSolver(const Eigen::MatrixXd& pointMatrix1,
	      const Eigen::MatrixXd& pointMatrix2,
	      const Eigen::MatrixXd& P);
  
  double solve(double& scaleOut,
	       Eigen::Matrix2d& rotationOut,
	       TranslationVector& translationOut);
private:
  void computeSMatrices();
  void computeMMatrices();
  void computeDiag();
  
  const Eigen::MatrixXd& pointMatrix1_;
  const Eigen::MatrixXd& pointMatrix2_;
  const Eigen::MatrixXd& P_;
  double NP_;
  Eigen::Vector2d muS_;
  Eigen::MatrixXd Shat_;
  Eigen::Vector2d muM_;
  Eigen::MatrixXd Mhat_;
  Eigen::MatrixXd diag_;
  Eigen::MatrixXd diag2_;
};
