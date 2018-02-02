#include "Utilities.hpp"

namespace Utilities
{

void
transform(const PointMatrix& pointMatrix,
          double scale,
          const RotationMatrix& rotation,
          const TranslationVector& translation,
          PointMatrix& transformedPointMatrix)
{
  transformedPointMatrix = scale * pointMatrix * rotation.transpose() + translation.replicate(pointMatrix.rows(), 1);
}

void
transform(const Eigen::MatrixXd& pointMatrix,
          double scale,
          const Eigen::Matrix2d& rotation,
          const TranslationVector& translation,
          Eigen::MatrixXd& transformedPointMatrix)
{
  transformedPointMatrix = scale * pointMatrix * rotation.transpose() + translation.replicate(pointMatrix.rows(), 1);
}

}
