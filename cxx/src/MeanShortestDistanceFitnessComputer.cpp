#include "MeanShortestDistanceFitnessComputer.hpp"

#include <utility>

using namespace std;

namespace
{
  double
  mean(const std::vector<double> v1)
  {
    if (v1.size() == 0)
    {
      return 0.0;
    }

    double sum = 0.0;
    for (double value : v1)
    {
      sum += value;
    }

    return sum / v1.size();
  }

  pair<vector<double>, vector<double> >
  computeShortestDistances(const PointMatrix& pointMatrix1,
                           const PointMatrix& pointMatrix2)
  {
    pair<vector<double>, vector<double> > shortestDistances;

    const int numRows1 = pointMatrix1.rows();
    const int numRows2 = pointMatrix2.rows();
    vector<double>& shortestFrom1 = shortestDistances.first;
    shortestFrom1.resize(numRows1, 1.0e10);
    vector<double>& shortestFrom2 = shortestDistances.second;
    shortestFrom2.resize(numRows2, 1.0e10);

    for (int rowIx1 = 0; rowIx1 < numRows1; ++rowIx1)
    {
      const double x1 = pointMatrix1(rowIx1, 0);
      const double y1 = pointMatrix1(rowIx1, 1);
      for (int rowIx2 = 0; rowIx2 < numRows2; ++rowIx2)
      {
        const double diffX = x1 - pointMatrix2(rowIx2, 0);
        const double diffY = y1 - pointMatrix2(rowIx2, 1);
        const double squareDistance = diffX * diffX + diffY * diffY;

        if (squareDistance < shortestFrom1[rowIx1])
        {
          shortestFrom1[rowIx1] = squareDistance;
        }
        if (squareDistance < shortestFrom2[rowIx2])
        {
          shortestFrom2[rowIx2] = squareDistance;
        }
      }
    }

    return shortestDistances;
  }
}

double MeanShortestDistanceFitnessComputer::compute(const PointMatrix& points1,
                                                    const PointMatrix& points2) const
{
  assert(points1.cols() == 2);
  assert(points2.cols() == 2);
  if (points1.rows() == 0
      || points2.rows() == 0)
    return 0.0;

  const pair<vector<double>, vector<double> > shortest =
    computeShortestDistances(points1, points2);
  return mean(shortest.first) + mean(shortest.second);
}
