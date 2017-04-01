#include "RigidSolver.hpp"

RigidSolver::RigidSolver(const Eigen::MatrixXd& pointMatrix1,
			 const Eigen::MatrixXd& pointMatrix2,
			 const Eigen::MatrixXd& P)
  : pointMatrix1_(pointMatrix1),
    pointMatrix2_(pointMatrix2),
    P_(P),
    NP_(0.0)
{}

double
RigidSolver::solve(double& scaleOut,
                   Eigen::Matrix2d& rotationOut,
                   TranslationVector& translationOut)
{
  NP_ = P_.sum();

  computeSMatrices();
  computeMMatrices();
  computeDiag();
 
  const Eigen::MatrixXd A = Shat_.transpose() * P_.transpose() * Mhat_;

  Eigen::JacobiSVD<Eigen::MatrixXd> svd(A, Eigen::ComputeFullV | Eigen::ComputeFullU);
  const Eigen::MatrixXd U = svd.matrixU();
  const Eigen::MatrixXd Vt = svd.matrixV().transpose(); 
  Eigen::Matrix2d C = Eigen::Matrix2d::Identity();
  C(1, 1) = (U * Vt).determinant();
  const Eigen::Matrix2d R = U * C * Vt;

  const double a = (A.transpose() * R).trace() / (Mhat_.transpose() * diag_ * Mhat_).trace();
  const Eigen::MatrixXd t = (muS_ - a * R * muM_).transpose();
  const double sigmaSquare = 1.0 / (2.0*NP_) * ((Shat_.transpose() * diag2_ * Shat_).trace() - a * (A.transpose() * R).trace());

  rotationOut = R;
  scaleOut = a;
  translationOut = t;
  
  return sigmaSquare;
}

void
RigidSolver::computeSMatrices()
{
  const Eigen::MatrixXd& M = pointMatrix1_;
  const Eigen::MatrixXd& S = pointMatrix2_;
  muS_ = S.transpose() * P_.transpose() * Eigen::MatrixXd::Constant(M.rows(), 1, 1.0) / NP_; // (2, 1) "mean" vector
  Shat_ = S - muS_.transpose().replicate(S.rows(), 1);
}

void
RigidSolver::computeMMatrices()
{
  const Eigen::MatrixXd& M = pointMatrix1_;
  const Eigen::MatrixXd& S = pointMatrix2_;
  muM_ = M.transpose() * P_ * Eigen::MatrixXd::Constant(S.rows(), 1, 1.0) / NP_; // (2, 1) "mean" vector
  Mhat_ = M - muM_.transpose().replicate(M.rows(), 1);
}

void
RigidSolver::computeDiag()
{
  const int num1Points = pointMatrix1_.rows();
  const int num2Points = pointMatrix2_.rows();
  
  diag_ = Eigen::MatrixXd::Zero(num1Points, num1Points);
  diag_.diagonal() = P_ * Eigen::MatrixXd::Constant(num2Points, 1, 1.0);
  
  diag2_ = Eigen::MatrixXd::Zero(num2Points, num2Points);
  diag2_.diagonal() = P_.transpose() * Eigen::MatrixXd::Constant(num1Points, 1, 1.0);
}
