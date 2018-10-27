#ifndef BruteForceMatcher_hpp
#define BruteForceMatcher_hpp

#include "Utilities.hpp"

class FitnessComputer;

class BruteForceMatcher
{
public:
  BruteForceMatcher(const FitnessComputer& fitnessComputer,
                    double* pointsReference,
                    int numRowsReference,
                    int numColsReference);

  void setCandidateKeepRatio(const int);

  void setCandidateDistanceTolerance(const double);

  void match(double* pointsToMatch,
             int numRowsToMatch,
             int numColsToMatch,
             double scale[1][1],
             double rotation[2][2],
             double translation[1][2],
             double fitness[1][1]);

private:
  double doMatch(const double* pointsToMatch,
                 const int numRowsToMatch,
                 const int numColsToMatch,
                 double& scaleOut,
                 RotationMatrix& rotationOut,
                 TranslationVector& translationOut) const;
  void computeTransformation(const Utilities::DoublePair& p1,
                             const Utilities::DoublePair& p2,
                             RotationMatrix& rotationOut,
                             TranslationVector& translationOut) const;

  EigVector referencePoint1_;
  EigVector referencePoint2_;
  double targetSquareDistance_;
  double targetDistanceTolerance_;

  const FitnessComputer& fitnessComputer_;
  int candidateKeepRatio_;
};

#endif
