#ifndef CoherentPointDriftMatcher2D_hpp
#define CoherentPointDriftMatcher2D_hpp

class CoherentPointDriftMatcher2D;

extern "C" {
  CoherentPointDriftMatcher2D* CoherentPointDriftMatcher2D_new();
  void CoherentPointDriftMatcher2D_delete(CoherentPointDriftMatcher2D*);
  void CoherentPointDriftMatcher2D_addPoint1(CoherentPointDriftMatcher2D*, double x, double y);
  void CoherentPointDriftMatcher2D_addPoint2(CoherentPointDriftMatcher2D*, double x, double y);
  void CoherentPointDriftMatcher2D_match(CoherentPointDriftMatcher2D*);
}

#endif