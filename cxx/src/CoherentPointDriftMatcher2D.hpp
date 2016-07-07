#ifndef CoherentPointDriftMatcher2D_hpp
#define CoherentPointDriftMatcher2D_hpp

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

extern "C" {
  CoherentPointDriftMatcher2D* CoherentPointDriftMatcher2D_new();
  void CoherentPointDriftMatcher2D_delete(CoherentPointDriftMatcher2D*);
  void CoherentPointDriftMatcher2D_addPoint1(CoherentPointDriftMatcher2D*, double x, double y);
  void CoherentPointDriftMatcher2D_addPoint2(CoherentPointDriftMatcher2D*, double x, double y);
  void CoherentPointDriftMatcher2D_match(CoherentPointDriftMatcher2D*);
}

#endif