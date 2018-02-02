#include "MostPopulatedCircleFinder.hpp"

MostPopulatedCircleFinder::MostPopulatedCircleFinder(double* points, int dim1, int dim2)
  : xMin_(std::numeric_limits<double>::max()),
    xMax_(-std::numeric_limits<double>::max()),
    yMin_(std::numeric_limits<double>::max()),
    yMax_(-std::numeric_limits<double>::max())
{
  assert(dim2 == 2);
  assert(0 == dim1 % 2);
  for (int i = 0; i < dim1; ++i)
  {
    addPoint(points[i*2], points[i*2+1]);
  }
}

void
MostPopulatedCircleFinder::addPoint(double x, double y)
{
  xy_.push_back(x);
  xy_.push_back(y);

  xMin_ = std::min(x, xMin_);
  xMax_ = std::max(x, xMax_);
  yMin_ = std::min(y, yMin_);
  yMax_ = std::max(y, yMax_);
}

OptionalPoint
MostPopulatedCircleFinder::get(double radius) const
{
  if (xy_.empty() || radius <= 0.0)
    return boost::none;

  const double radiusSquare = radius*radius;
  const size_t step = 1;
  const size_t xLength = xMax_ - xMin_ + 1;
  const size_t yLength = yMax_ - yMin_ + 1;

  double maxHitsX = 0.0;
  double maxHitsY = 0.0;
  int maxHits = 0;

  for (size_t xCircleIx = 0; xCircleIx < xLength; xCircleIx += step)
  {
    const double xCircle = xMin_ + xCircleIx;
    for (size_t yCircleIx = 0; yCircleIx < yLength; yCircleIx += step)
    {
      const double yCircle = yMin_ + yCircleIx;

      int numHits = 0;
      for (size_t ix = 0; ix < xy_.size(); ix += 2)
      {
        const double xDiff = xCircle - xy_[ix];
        const double yDiff = yCircle - xy_[ix+1];

        if (radius < xDiff || radius < -xDiff)
          continue;

        if (radius < yDiff || radius < -yDiff)
          continue;

        const double diffSquare = xDiff*xDiff + yDiff*yDiff;
        if (diffSquare <= radiusSquare)
          ++numHits;
      }

      if (numHits > maxHits)
      {
        maxHits = numHits;
        maxHitsX = xCircle;
        maxHitsY = yCircle;
      }
    }
  }

  return std::make_pair(maxHitsX, maxHitsY);
}

