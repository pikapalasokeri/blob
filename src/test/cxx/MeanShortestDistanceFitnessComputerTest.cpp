#include "catch.hpp"
#include "MeanShortestDistanceFitnessComputer.hpp"
#include "TestUtilities.hpp"

TEST_CASE("MSDFC: No points - zero fitness", "[MeanShortestDistanceFitnessComputer]")
{
  PointMatrix empty;
  const MeanShortestDistanceFitnessComputer c(empty);
  CHECK(c.compute(empty) == 0.0);
}

TEST_CASE("MSDFC: One point matrix - zero fitness", "[MeanShortestDistanceFitnessComputer]")
{
  const PointMatrix points(10, 2);
  const MeanShortestDistanceFitnessComputer c1(points);
  CHECK(c1.compute(PointMatrix()) == 0.0);

  const PointMatrix empty;
  const MeanShortestDistanceFitnessComputer c2(empty);
  CHECK(c2.compute(PointMatrix(10, 2)) == 0.0);
}

TEST_CASE("MSDFC: Rectangle of points", "[MeanShortestDistanceFitnessComputer]")
{
  PointMatrix points1(2, 2);
  points1 << 0.0, 0.0,
             0.0, 2.0;

  PointMatrix points2(2, 2);
  points2 << 1.0, 0.0,
             1.0, 2.0;
  const MeanShortestDistanceFitnessComputer c(points2);
  CHECK(c.compute(points1) == 2.0);
}

TEST_CASE("MSDFC: Asymmetric square of points", "[MeanShortestDistanceFitnessComputer]")
{
  PointMatrix points1(1, 2);
  points1 << 0.0, 0.0;

  PointMatrix points2(3, 2);
  points2 << 1.0, 0.0,
             0.0, 1.0,
             1.0, 1.0;
  const MeanShortestDistanceFitnessComputer c(points2);
  // 2a  2b
  //
  // 1   2c

  // 1  -> 2x: distance 1
  // 2a -> 1:  distance 1
  // 2b -> 1:  distance sqrt(2) = 1.41...
  // 2c -> 1:  distance 1
  // sum of means: 1^2 + (1^2 + sqrt(2)^2 + 1^2)/3 = 1 + 4/3 = 2.3333
  CHECK_THAT(c.compute(points1), isCloseEnoughTo(2.33333));
}

TEST_CASE("MSDFC: Asymmetric square plus one way off", "[MeanShortestDistanceFitnessComputer]")
{
  PointMatrix points1(2, 2);
  points1 << 0.0, 0.0,   // a
             1.0, -10.0; // b

  PointMatrix points2(3, 2);
  points2 << 1.0, 0.0, // c
             0.0, 1.0, // a
             1.0, 1.0; // b
  const MeanShortestDistanceFitnessComputer c(points2);

  // 2a  2b
  //
  // 1a  2c
  //
  //
  //     1b

  // 1a -> 2x: distance 1
  // 1b -> 2x: distance 10
  // 2a -> 1x: distance 1
  // 2b -> 1x: distance sqrt(2) = 1.41...
  // 2c -> 1x: distance 1
  // sum of means: (1^2 + 10^2)/2 + (1^2 + sqrt(2)^2 + 1^2)/3 = 101/2 + 4/3 = 50.5 + 1.33333 = 51.83333
  CHECK_THAT(c.compute(points1), isCloseEnoughTo(51.83333));
}
