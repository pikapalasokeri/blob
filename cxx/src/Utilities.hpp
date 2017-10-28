#include <Eigen/Dense>

#include "EigenDefs.hpp"

namespace Utilities
{
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
}
