#ifndef MostPopulatedCircleFinder_hpp
#define MostPopulatedCircleFinder_hpp

#include <limits>
#include <vector>
#include <utility>

using Point = std::pair<double, double>;

class MostPopulatedCircleFinder
{
public:
  MostPopulatedCircleFinder()
    : xMin_(std::numeric_limits<double>::max()),
      xMax_(-std::numeric_limits<double>::max()),
      yMin_(std::numeric_limits<double>::max()),
      yMax_(-std::numeric_limits<double>::max())
      {}

  MostPopulatedCircleFinder(double*, int, int);

  void addPoint(double x, double y);

  Point get(double radius) const;

private:
  std::vector<double> xy_;
  double xMin_;
  double xMax_;
  double yMin_;
  double yMax_;
};

#endif
