#include "CoherentPointDriftMatcher2D.hpp"
#include "../CoherentPointDriftMatcher2DImpl.hpp"

extern "C" {
  CoherentPointDriftMatcher2D* CoherentPointDriftMatcher2D_new()
  {
    return new CoherentPointDriftMatcher2D();
  }

  void CoherentPointDriftMatcher2D_delete(CoherentPointDriftMatcher2D* matcher)
  {
    delete matcher;
  }

  void CoherentPointDriftMatcher2D_addPoint1(CoherentPointDriftMatcher2D* matcher, double x, double y)
  {
    matcher->addPoint1(x,y);
  }

  void CoherentPointDriftMatcher2D_addPoint2(CoherentPointDriftMatcher2D* matcher, double x, double y)
  {
    matcher->addPoint2(x,y);
  }

  void CoherentPointDriftMatcher2D_match(CoherentPointDriftMatcher2D* matcher)
  {
    matcher->match();
  }
}
