#include "MostPopulatedCircleFinder.hpp"
#include "catch.hpp"
#include "TestUtilities.hpp"
#include <sstream>

using Point = std::pair<double, double>;

namespace Catch
{
  template<> struct StringMaker<Point>
  {
    static std::string convert(const Point& p)
    {
      std::ostringstream ss;
      ss << "(" << p.first << ", " << p.second << ")";
      return ss.str();
    }
  };
}

TEST_CASE("No points", "[MostPopulatedCircleFinder]")
{
  MostPopulatedCircleFinder finder;
  const OptionalPoint p = finder.get(0.02);
  CHECK(!p);
}

TEST_CASE("Bad radius", "[MostPopulatedCircleFinder]")
{
  MostPopulatedCircleFinder finder;
  finder.addPoint(0.0, 0.0);
  finder.addPoint(1.0, 1.0);

  const OptionalPoint p1 = finder.get(0.0);
  CHECK(!p1);

  const OptionalPoint p2 = finder.get(-1.0);
  CHECK(!p2);
}

TEST_CASE("One point", "[MostPopulatedCircleFinder]")
{
  MostPopulatedCircleFinder finder;
  finder.addPoint(1.0, 1.0);

  const double radius = 0.1;
  const OptionalPoint circleCenter = finder.get(radius);

  REQUIRE(bool(circleCenter));
  CHECK_THAT(std::make_pair(1.0, 1.0), isInside(*circleCenter, radius));
}

TEST_CASE("Three points - small radius", "[MostPopulatedCircleFinder]")
{
  MostPopulatedCircleFinder finder;
  const Point p1(0.0, 0.0);
  const Point p2(3.0, 0.0);
  const Point p3(4.0, 0.0);
  finder.addPoint(p1.first, p1.second);
  finder.addPoint(p2.first, p2.second);
  finder.addPoint(p3.first, p3.second);

  const double radius = 1.0;
  const OptionalPoint circleCenter = finder.get(radius);

  REQUIRE(bool(circleCenter));
  CHECK_THAT(p1, !isInside(*circleCenter, radius));
  CHECK_THAT(p2, isInside(*circleCenter, radius));
  CHECK_THAT(p3, isInside(*circleCenter, radius));
}

TEST_CASE("Three points - large radius", "[MostPopulatedCircleFinder]")
{
  MostPopulatedCircleFinder finder;
  const Point p1(0.0, 0.0);
  const Point p2(2.0, 0.0);
  const Point p3(3.0, 0.0);
  finder.addPoint(p1.first, p1.second);
  finder.addPoint(p2.first, p2.second);
  finder.addPoint(p3.first, p3.second);

  const double radius = 2.0;
  const OptionalPoint circleCenter = finder.get(radius);

  REQUIRE(bool(circleCenter));
  CHECK_THAT(p1, isInside(*circleCenter, radius));
  CHECK_THAT(p2, isInside(*circleCenter, radius));
  CHECK_THAT(p3, isInside(*circleCenter, radius));
}

TEST_CASE("Many points over large area", "[MostPopulatedCircleFinder]")
{
  MostPopulatedCircleFinder finder;
  for (double x = 0.0; x < 100; x += 2.0)
  {
    for (double y = 0.0; y < 100; y += 2.0)
    {
      finder.addPoint(x, y);
    }
  }

  const double radius = 25.0;
  const OptionalPoint circleCenter = finder.get(radius);
  REQUIRE(bool(circleCenter));
}

TEST_CASE("Corner", "[MostPopulatedCircleFinder]")
{
  MostPopulatedCircleFinder finder;
  const Point p1(0.0, 0.0);
  const Point p2(1.0, 0.0);
  const Point p3(0.0, 1.0);
  finder.addPoint(p1.first, p1.second);
  finder.addPoint(p2.first, p2.second);
  finder.addPoint(p3.first, p3.second);

  const double radius = 1.0;
  const OptionalPoint circleCenter = finder.get(radius);

  REQUIRE(bool(circleCenter));
  CHECK_THAT(p1, isInside(*circleCenter, radius));
  CHECK_THAT(p2, isInside(*circleCenter, radius));
  CHECK_THAT(p3, isInside(*circleCenter, radius));
  CHECK(circleCenter->first == 0.0);
  CHECK(circleCenter->second == 0.0);
}

TEST_CASE("Non-integer coordinates", "[MostPopulatedCircleFinder]")
{
  MostPopulatedCircleFinder finder;
  const Point p1(0.5, 0.5);
  const Point p2(1.0, 0.0);
  const Point p3(1.0, 1.0);
  finder.addPoint(p1.first, p1.second);
  finder.addPoint(p2.first, p2.second);
  finder.addPoint(p3.first, p3.second);

  const double radius = 1.0;
  const OptionalPoint circleCenter = finder.get(radius);

  REQUIRE(bool(circleCenter));
  CHECK_THAT(p1, isInside(*circleCenter, radius));
  CHECK_THAT(p2, isInside(*circleCenter, radius));
  CHECK_THAT(p3, !isInside(*circleCenter, radius));
  CHECK(circleCenter->first == 0.5);
  CHECK(circleCenter->second == 0.0);
}
