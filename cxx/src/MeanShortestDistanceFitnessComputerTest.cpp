#include "catch.hpp"
#include "MeanShortestDistanceFitnessComputer.hpp"
#include "TestUtilities.hpp"

TEST_CASE("No points - zero fitness", "[MeanShortestDistanceFitnessComputer]")
{
  const MeanShortestDistanceFitnessComputer c;
  CHECK(c.compute(PointMatrix(), PointMatrix()) == 0.0);
}

TEST_CASE("One point matrix - zero fitness", "[MeanShortestDistanceFitnessComputer]")
{
  const MeanShortestDistanceFitnessComputer c;
  CHECK(c.compute(PointMatrix(), PointMatrix(10, 2)) == 0.0);
  CHECK(c.compute(PointMatrix(10, 2), PointMatrix()) == 0.0);
}

TEST_CASE("Rectangle of points", "[MeanShortestDistanceFitnessComputer]")
{
  const MeanShortestDistanceFitnessComputer c;
  PointMatrix points1(2, 2);
  points1 << 0.0, 0.0,
             0.0, 2.0;

  PointMatrix points2(2, 2);
  points2 << 1.0, 0.0,
             1.0, 2.0;

  CHECK(c.compute(points1, points2) == 2.0);
}

TEST_CASE("Asymmetric square of points", "[MeanShortestDistanceFitnessComputer]")
{
  const MeanShortestDistanceFitnessComputer c;
  PointMatrix points1(1, 2);
  points1 << 0.0, 0.0;

  PointMatrix points2(3, 2);
  points2 << 1.0, 0.0,
             0.0, 1.0,
             1.0, 1.0;
  // 2a  2b
  //
  // 1   2c

  // 1  -> 2x: distance 1
  // 2a -> 1:  distance 1
  // 2b -> 1:  distance sqrt(2) = 1.41...
  // 2c -> 1:  distance 1
  // sum of means: 1^2 + (1^2 + sqrt(2)^2 + 1^2)/3 = 1 + 4/3 = 2.3333
  CHECK_THAT(c.compute(points1, points2), isCloseEnoughTo(2.33333));
}

TEST_CASE("Asymmetric square plus one way off", "[MeanShortestDistanceFitnessComputer]")
{
  const MeanShortestDistanceFitnessComputer c;
  PointMatrix points1(2, 2);
  points1 << 0.0, 0.0,   // a
             1.0, -10.0; // b

  PointMatrix points2(3, 2);
  points2 << 1.0, 0.0, // c
             0.0, 1.0, // a
             1.0, 1.0; // b
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
  CHECK_THAT(c.compute(points1, points2), isCloseEnoughTo(51.83333));
}
