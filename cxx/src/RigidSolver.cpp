#include "RigidSolver.hpp"

RigidSolver::RigidSolver(const Eigen::MatrixXd& pointMatrix1,
			 const Eigen::MatrixXd& pointMatrix2,
			 const Eigen::MatrixXd& P,
			 double scale,
			 const Eigen::Matrix2d& rotation,
			 const TranslationVector& translation)
  : pointMatrix1_(pointMatrix1),
    pointMatrix2_(pointMatrix2),
    P_(P),
    scale_(scale),
    rotation_(rotation),
    translation_(translation)
{}

double
RigidSolver::solve(double& scaleOut,
		   Eigen::Matrix2d& rotationOut,
		   TranslationVector& translationOut)
{
  const int num1Points = pointMatrix1_.rows();
  const int num2Points = pointMatrix2_.rows();
  
  const Eigen::MatrixXd& M = pointMatrix1_;
  const Eigen::MatrixXd& S = pointMatrix2_;

  const double NP = P_.sum();
  const Eigen::Vector2d muS = S.transpose() * P_.transpose() * Eigen::MatrixXd::Constant(num1Points, 1, 1.0) / NP; // (2, 1) "mean" vector
  const Eigen::Vector2d muM = M.transpose() * P_ * Eigen::MatrixXd::Constant(num2Points, 1, 1.0) / NP; // (2, 1) "mean" vector

  const Eigen::MatrixXd Shat = S - muS.transpose().replicate(num2Points, 1);
  const Eigen::MatrixXd Mhat = M - muM.transpose().replicate(num1Points, 1);
  const Eigen::MatrixXd A = Shat.transpose() * P_.transpose() * Mhat;

  Eigen::JacobiSVD<Eigen::MatrixXd> svd(A, Eigen::ComputeFullV | Eigen::ComputeFullU);
  const Eigen::MatrixXd U = svd.matrixU();
  const Eigen::MatrixXd Vt = svd.matrixV().transpose(); 
  const Eigen::MatrixXd shapeSigma = svd.singularValues();
  
  Eigen::Matrix2d C = Eigen::Matrix2d::Identity();
  C(1, 1) = (U * Vt).determinant();

  const Eigen::Matrix2d R = U * C * Vt;

  Eigen::MatrixXd x = P_ * Eigen::MatrixXd::Constant(num2Points, 1, 1.0);
  Eigen::MatrixXd diag = Eigen::MatrixXd::Zero(x.rows(), x.rows());
  diag.diagonal() = x;
  
  const double a = (A.transpose() * R).trace() / (Mhat.transpose() * diag * Mhat).trace();
  
  const Eigen::MatrixXd t = (muS - a * R * muM).transpose();

  x = P_.transpose() * Eigen::MatrixXd::Constant(num1Points, 1, 1.0);
  diag.diagonal() = x;

  const double sigmaSquare = 1.0 / (2.0*NP) * ((Shat.transpose() * diag * Shat).trace() - a * (A.transpose() * R).trace());

  
  rotationOut = R;
  scaleOut = a;
  translationOut = t;
  
  return sigmaSquare;
}
