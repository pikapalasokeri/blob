#ifndef CoherentPointDriftMatcherImpl_hpp
#define CoherentPointDriftMatcherImpl_hpp

#include <vector>
#include <utility>

class CoherentPointDriftMatcher2D
{
public:
  CoherentPointDriftMatcher2D();

  ~CoherentPointDriftMatcher2D();

  void addPoint1(double x, double y);

  void addPoint2(double x, double y);

  void match();

private:
  typedef std::pair<double, double> DoublePair;
  typedef std::vector<DoublePair> PointVector;
  PointVector pointSet1_;
  PointVector pointSet2_;
};

#endif