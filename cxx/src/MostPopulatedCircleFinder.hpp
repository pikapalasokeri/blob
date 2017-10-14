#ifndef MostPopulatedCircleFinder_hpp
#define MostPopulatedCircleFinder_hpp

#include <utility>
#include <boost/optional.hpp>

using OptionalPoint = boost::optional<std::pair<double, double> >;

class MostPopulatedCircleFinder
{
public:
  MostPopulatedCircleFinder()
    : xMin_(std::numeric_limits<double>::max()),
      xMax_(-std::numeric_limits<double>::max()),
      yMin_(std::numeric_limits<double>::max()),
      yMax_(-std::numeric_limits<double>::max())
  {}

  void addPoint(double x, double y);

  OptionalPoint get(double radius) const;

private:
  std::vector<double> xy_;
  double xMin_;
  double xMax_;
  double yMin_;
  double yMax_;
};

#endif
