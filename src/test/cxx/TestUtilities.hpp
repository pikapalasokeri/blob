#ifndef TestUtilities_hpp
#define TestUtilities_hpp

#include "catch.hpp"
#include <Eigen/Dense>
#include <cmath>

inline bool closeEnough(double v1, double v2, double tol = 1.0e-6)
{
  return std::abs(v1 - v2) < tol;
}

template <class Type>
bool closeEnough(const Type& m1, const Type& m2, double tolerance = 1.0e-6)
{
  if (m1.rows() != m2.rows()
      || m1.cols() != m2.cols())
    return false;

  bool result = true;
  for (int i = 0; i < m1.rows(); ++i)
  {
    for (int j = 0; j < m1.cols(); ++j)
    {
      result &= closeEnough(m1(i, j), m2(i, j), tolerance);
    }
  }
  return result;
}

inline bool isRotationMatrix(const Eigen::Matrix2d& matrix)
{
  bool result = true;
  result &= matrix(0, 0) == matrix(1, 1);
  result &= matrix(1, 0) == -matrix(0, 1);
  result &= closeEnough(matrix(0, 0)*matrix(0,0) + matrix(1, 0)*matrix(1, 0),
                        1.0);
  return result;
}

template <class Type>
class ApproximateComparison : public Catch::MatcherBase<Type>
{
public:
  ApproximateComparison(const Type& reference, double tolerance)
    : reference_(reference),
      tolerance_(tolerance)
  {}

  virtual bool match(const Type& actual) const override
  {
    return closeEnough(actual, reference_, tolerance_);
  }

  virtual std::string describe() const override
  {
    std::ostringstream ss;
    ss << "\ncompare with reference\n" << reference_;
    return ss.str();
  }

private:
  const Type& reference_;
  const double tolerance_;
};

template <class Type>
ApproximateComparison<Type>
isCloseEnoughTo(const Type& reference, double tolerance = 1.0e-5)
{
  return ApproximateComparison<Type>(reference, tolerance);
}

class IsInsideComparison : public Catch::MatcherBase<std::pair<double, double> >
{
public:
  IsInsideComparison(std::pair<double, double> circleCenter,
                     double radius)
    : circleCenter_(circleCenter),
      radius_(radius)
  {}

  virtual bool match(const std::pair<double, double>& point) const override
  {
    const double xDiff = point.first - circleCenter_.first;
    const double yDiff = point.second - circleCenter_.second;
    return xDiff*xDiff + yDiff*yDiff <= radius_*radius_;
  }

  virtual std::string describe() const override
  {
    std::ostringstream ss;
    ss << "is inside circle ("
       << circleCenter_.first << ", "
       << circleCenter_.second << ", "
       << radius_ << ")";
    return ss.str();
  }

private:
  const std::pair<double, double> circleCenter_;
  const double radius_;
};

inline IsInsideComparison
isInside(std::pair<double, double> circleCenter,
         double radius)
{
  return IsInsideComparison(circleCenter, radius);
}

#endif
