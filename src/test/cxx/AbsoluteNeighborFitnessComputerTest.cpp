#include "catch.hpp"
#include "AbsoluteNeighborFitnessComputer.hpp"
#include "TestUtilities.hpp"

#include <limits>

TEST_CASE("ANFC One empty point matrix - 100% fitness", "[AbsoluteNeighborFitnessComputer]")
{
  const PointMatrix points(10, 2);
  const AbsoluteNeighborFitnessComputer c1(points, 1.0);
  CHECK(c1.compute(PointMatrix()) == 1.0);

  const PointMatrix empty;
  const AbsoluteNeighborFitnessComputer c2(empty, 1.0);
  CHECK(c2.compute(PointMatrix(10, 2)) == 1.0);
}

TEST_CASE("ANFC tolerance <= 0 - 100% fitness", "[AbsoluteNeighborFitnessComputer]")
{
  const PointMatrix points(10, 2);
  const AbsoluteNeighborFitnessComputer c1(points, 0.0);
  CHECK(c1.compute(points) == 1.0);

  const AbsoluteNeighborFitnessComputer c2(points, -0.1);
  CHECK(c2.compute(points) == 1.0);
}

TEST_CASE("ANFC Rectangle of points", "[AbsoluteNeighborFitnessComputer]")
{
  PointMatrix points1(2, 2);
  points1 << 0.0, 0.0,
             0.0, 2.0;

  PointMatrix points2(2, 2);
  points2 << 1.0, 0.0,
             1.0, 2.0;
  const AbsoluteNeighborFitnessComputer c1(points2, 1.0001);
  CHECK(c1.compute(points1) == 0.0);

  const AbsoluteNeighborFitnessComputer c2(points2, 0.9999);
  CHECK(c2.compute(points1) == 1.0);
}

TEST_CASE("ANFC Asymmetric square of points", "[AbsoluteNeighborFitnessComputer]")
{
  PointMatrix points1(1, 2);
  points1 << 0.0, 0.0;

  PointMatrix refPoints(3, 2);
  refPoints << 1.0, 0.0,
               0.0, 1.0,
               1.0, 1.0;
  const AbsoluteNeighborFitnessComputer c0(refPoints, 0.5);
  CHECK(c0.compute(points1) == 1.0);

  const AbsoluteNeighborFitnessComputer c2(refPoints, 1.0);
  CHECK_THAT(c2.compute(points1), isCloseEnoughTo(1/3.0));

  const AbsoluteNeighborFitnessComputer c3(refPoints, 1.5);
  CHECK(c3.compute(points1) == 0.0);
}
