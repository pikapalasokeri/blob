#ifndef Random_hpp
#define Random_hpp

#include <random>

template<class Distribution>
class MersenneTwister
{
public:
  MersenneTwister()
    : mersenneTwisterEngine_(0761306430)
  {}

  double getNext()
  {
    return distribution_(mersenneTwisterEngine_);
  }

private:
  Distribution distribution_;
  std::mt19937_64 mersenneTwisterEngine_;
};

/*
class StandardNormalDistributionNumberGenerator
{
public:
  StandardNormalDistributionNumberGenerator()
    : mersenneTwisterEngine_(0761306430)
  {}

  double getNext()
  {
    return distribution_(mersenneTwisterEngine_);
  }

private:
  std::normal_distribution<double> distribution_;
  std::mt19937_64 mersenneTwisterEngine_;
};
*/

#endif
