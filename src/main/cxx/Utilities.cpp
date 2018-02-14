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

  PointMatrix
  toPointMatrix(const double* points, int dim1, int dim2)
  {
    PointMatrix result(dim1, dim2);
    for (int i = 0; i < dim1; ++i)
    {
      for (int j = 0; j < dim2; ++j)
      {
        result(i, j) = points[i * dim2 + j];
      }
    }

    return result;
  }
}
