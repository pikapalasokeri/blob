import numpy as np
from timeit import default_timer as timer
from numpy.core.umath_tests import inner1d

'''
https://en.wikipedia.org/wiki/Point_set_registration#Coherent_point_drift
'''
class CoherentPointDriftMatcher2D:
  def __init__(self, pointSet1, pointSet2):
    self._pointSet1 = pointSet1
    self._pointSet2 = pointSet2

  def match(self, w):
    theta = (1.0, np.eye(2), np.zeros((1,2)))
    sigmaSquare = self._computeSigmaSquare()

    P = np.zeros((self._pointSet1.shape[0], self._pointSet2.shape[0]))

    tiledJPoints = []
    numIPoints = self._pointSet1.shape[0]
    for jPoint in self._pointSet2:
      tiledJPoints.append(np.tile(jPoint, (numIPoints, 1)))
    
    numJPoints = self._pointSet2.shape[0]
    numerators = np.zeros((numIPoints, numJPoints))
    denominators = np.zeros((numIPoints, numJPoints))

    registered = False
    ix = 0
    oldSigmaSquare = 1.0e+10; # should be large enough
    while not registered:
      start = timer()
      print ix
      ix += 1

      sigmaSquareChange = abs(oldSigmaSquare - sigmaSquare)
      oldSigmaSquare = sigmaSquare
      print "Change in sigmaSquare:", sigmaSquareChange
      print "scale:", theta[0]
      print "rotation:", theta[1]
      print "translation:", theta[2]
      print "sigmaSquare:", sigmaSquare
      if ix == 100 or sigmaSquare < 0.0 or (ix > 50 and sigmaSquareChange < 0.001):
        return theta[0], theta[1], theta[2]
      transformedPointSet1 = transform(theta[0], theta[1], theta[2], self._pointSet1)
      constant1 = -1.0/(2.0*sigmaSquare)
      constant2 = (2.0*np.pi*sigmaSquare) * w / (1 - w) * self._pointSet1.shape[0]/self._pointSet2.shape[0]

      
      for j in range(numJPoints):
        jPoints = tiledJPoints[j]
        sjTmkDiffs = jPoints - transformedPointSet1
        diffSquares = inner1d(sjTmkDiffs, sjTmkDiffs)
        exponents = constant1 * diffSquares
        termsInDenominatorSum = np.exp(exponents)
        denominatorSum = np.sum(termsInDenominatorSum)
        denominators[:,j] = denominatorSum
      
      for i in range(numIPoints):
        for j, jPoint in enumerate(self._pointSet2):
          sjTmiDiff = jPoint - transformedPointSet1[i]
          numerators[i,j] = np.exp(constant1 * np.dot(sjTmiDiff, sjTmiDiff))

      denominators += constant2
      P = numerators / denominators

      print "Normalized sum(P):", np.sum(np.sum(P))/(numIPoints*numJPoints)
      print "MeanMax(P,0)", np.mean(np.max(P,axis=0))
      print "MeanMax(P,1)", np.mean(np.max(P,axis=1))
      print "MedianMax(P,0)", np.median(np.max(P,axis=0))
      print "MedianMax(P,1)", np.median(np.max(P,axis=1))
      

      end = timer()
      print "loop:", end-start
      theta, sigmaSquare = self._solveRigid(P)

      print theta, sigmaSquare

  def _computeSigmaSquare(self):
    sum = 0.0
    # TODO: Make this more efficient
    for point1 in self._pointSet1:
      for point2 in self._pointSet2:
        diff = point1 - point2
        sum += np.dot(diff, diff)
    return sum/(2.0*self._pointSet1.shape[0]*self._pointSet2.shape[0])

  def _solveRigid(self, P):
    start = timer()
    M = self._pointSet1
    S = self._pointSet2

    NP = np.dot(np.dot(np.ones((1, P.shape[0])), P), np.ones((P.shape[1], 1))) # Sum of all elements in P matrix
    muS = 1.0/(NP) * np.dot(S.transpose(), np.dot(P.transpose(), np.ones((P.shape[0], 1)))) # (2,1) "mean" vector
    muM = 1.0/(NP) * np.dot(M.transpose(), np.dot(P, np.ones((P.shape[1], 1))))             # (2,1) "mean" vector

    Shat = S - muS.transpose()
    Mhat = M - muM.transpose()

    A = np.dot(np.dot(Shat.transpose(), P.transpose()), Mhat)

    U, shapeSigma, Vt = np.linalg.svd(A)

    C = np.eye(2)
    C[-1:-1] = np.linalg.det(np.dot(U, Vt))

    R = np.dot(U, np.dot(C, Vt))

    diag = np.diag(np.squeeze(np.dot(P, np.ones((P.shape[1], 1)))))

    a = np.trace(np.dot(A.transpose(), R)) / np.trace(np.dot(Mhat.transpose(), np.dot(diag, Mhat)))
    t = (muS - a*np.dot(R, muM)).transpose()

    diag = np.diag(np.squeeze(np.dot(P.transpose(), np.ones((P.shape[0], 1)))))
    sigmaSquare = 1.0/(2.0*NP) * (np.trace(np.dot(Shat.transpose(), np.dot(diag, Shat))) - a * np.trace(np.dot(A.transpose(), R)))
    
    end = timer()
    print "one iteration _solveRigid:", end-start
    return (a, R, t), sigmaSquare

def transform(scale, rotation, translation, points):
  return scale*np.dot(points, rotation.transpose()) + translation

