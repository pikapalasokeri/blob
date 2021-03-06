#include <Eigen/Dense>

#include "EigenDefs.hpp"
#include <vector>

namespace Utilities
{
  using DoublePair = std::pair<double, double>;
  using PointVector = std::vector<DoublePair>;

  void
  transform(const PointMatrix& pointMatrix,
            double scale,
            const RotationMatrix& rotation,
            const TranslationVector& translation,
            PointMatrix& transformedPointMatrix);

  void
  transform(const Eigen::MatrixXd& pointMatrix,
            double scale,
            const Eigen::Matrix2d& rotation,
            const TranslationVector& translation,
            Eigen::MatrixXd& transformedPointMatrix);

  PointMatrix
  toPointMatrix(const double* points, int dim1, int dim2);
}
