#ifndef CoherentPointDriftMatcherImpl_hpp
#define CoherentPointDriftMatcherImpl_hpp

#include <iostream>

class CoherentPointDriftMatcher2D
{
public:
  CoherentPointDriftMatcher2D()
  {
    std::cout << "Constructing." << std::endl;
  }

  ~CoherentPointDriftMatcher2D()
  {
    std::cout << "Destroying." << std::endl;
  }
};

#endif