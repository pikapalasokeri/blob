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
}
