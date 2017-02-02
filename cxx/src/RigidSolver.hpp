#include "EigenDefs.hpp"
#include <Eigen/Dense>

class RigidSolver
{
public:
  RigidSolver(const Eigen::MatrixXd& pointMatrix1,
	      const Eigen::MatrixXd& pointMatrix2,
	      const Eigen::MatrixXd& P,
	      double scale,
	      const Eigen::Matrix2d& rotation,
	      const TranslationVector& translation);
  
  double solve(double& scaleOut,
	       Eigen::Matrix2d& rotationOut,
	       TranslationVector& translationOut);
private:
  const Eigen::MatrixXd& pointMatrix1_;
  const Eigen::MatrixXd& pointMatrix2_;
  const Eigen::MatrixXd& P_;
  double scale_;
  const Eigen::Matrix2d& rotation_;
  const TranslationVector& translation_;
};
