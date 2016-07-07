#include "CoherentPointDriftMatcher2D.hpp"

#include <iostream>

CoherentPointDriftMatcher2D::CoherentPointDriftMatcher2D()
{
  std::cout << __TIME__  << std::endl;
  std::cout << "Constructing." << std::endl;
}

CoherentPointDriftMatcher2D::~CoherentPointDriftMatcher2D()
{
  std::cout << "Destroying." << std::endl;
}

void
CoherentPointDriftMatcher2D::addPoint1(double x, double y)
{
  pointSet1_.emplace_back(x, y);
}

void
CoherentPointDriftMatcher2D::addPoint2(double x, double y)
{
  pointSet2_.emplace_back(x, y);
}

void
CoherentPointDriftMatcher2D::match(double* scale, double* rotation, double* translation)
{
  std::cout << "match():" << std::endl;
  std::cout << "  scale: " << scale[0] << std::endl
            << "  rotation: " << rotation[0] << " " << rotation[1] << std::endl
            << "            " << rotation[2] << " " << rotation[3] << std::endl
            << "  translation: " << translation[0] << " " << translation[1] << std::endl;
}

void
CoherentPointDriftMatcher2D::output()
{
  std::cout << "CoherentPointDriftMatcher2D:" << std::endl;

  std::cout << "  pointSet1_:" << std::endl;
  for (auto point : pointSet1_)
  {
    std::cout << "    " << point.first << " " << point.second << std::endl;
  }

  std::cout << "  pointSet2_:" << std::endl;
  for (auto point : pointSet2_)
  {
    std::cout << "    " << point.first << " " << point.second << std::endl;
  }  
}


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

  void CoherentPointDriftMatcher2D_match(CoherentPointDriftMatcher2D* matcher, double* scale, double* rotation, double* translation)
  {
    matcher->match(scale, rotation, translation);
  }

  void CoherentPointDriftMatcher2D_output(CoherentPointDriftMatcher2D* matcher)
  {
    matcher->output();
  }
}
