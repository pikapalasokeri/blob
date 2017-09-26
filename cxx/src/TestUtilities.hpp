#include <Eigen/Dense>
#include <cmath>

bool closeEnough(double v1, double v2, double tol = 1.0e-6)
{
  return std::abs(v1 - v2) < tol;
}

template <class MatrixType>
bool closeEnough(const MatrixType& m1, const MatrixType& m2, double tolerance = 1.0e-6)
{
  if (m1.rows() != m2.rows()
      || m1.cols() != m2.cols())
    return false;

  bool result = true;
  for (int i = 0; i < m1.rows(); ++i)
  {
    for (int j = 0; j < m1.cols(); ++j)
    {
      result &= closeEnough(m1(i, j), m2(i, j), tolerance);
    }
  }
  return result;
}

bool isRotationMatrix(const Eigen::Matrix2d& matrix)
{
  bool result = true;
  result &= matrix(0, 0) == matrix(1, 1);
  result &= matrix(1, 0) == -matrix(0, 1);
  result &= closeEnough(matrix(0, 0)*matrix(0,0) + matrix(1, 0)*matrix(1, 0),
                        1.0);
  return result;
}

template <class MatrixType>
class MatrixComparison : public Catch::MatcherBase<MatrixType>
{
public:
  MatrixComparison(const MatrixType& referenceMatrix, double tolerance)
    : referenceMatrix_(referenceMatrix),
      tolerance_(tolerance)
  {}

  virtual bool match(const MatrixType& matrix) const override
  {
    return closeEnough(matrix, referenceMatrix_, tolerance_);
  }

  virtual std::string describe() const
  {
    std::ostringstream ss;
    ss << "\ncompare matrix with reference\n" << referenceMatrix_;
    return ss.str();
  }

private:
  const MatrixType& referenceMatrix_;
  const double tolerance_;
};

template <class MatrixType>
MatrixComparison<MatrixType> isCloseEnoughTo(const MatrixType& referenceMatrix)
{
  const double tolerance = 1.0e-5;
  return MatrixComparison<MatrixType>(referenceMatrix, tolerance);
}

