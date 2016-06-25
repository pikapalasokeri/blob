#!/usr/bin/python

from scipy import misc
from scipy import ndimage
import numpy as np
from numpy.core.umath_tests import inner1d
import matplotlib.pyplot as plt
from EdgeDetector import *
from timeit import default_timer as timer

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
      if ix == 250 or sigmaSquare < 0.0 or (ix > 50 and sigmaSquareChange < 0.001):
        return theta[0], theta[1], theta[2]
      transformedPointSet1 = transform(theta[0], theta[1], theta[2], self._pointSet1)
      
      constant1 = -1.0/(2.0*sigmaSquare)
      constant2 = (2.0*np.pi*sigmaSquare) * w / (1 - w) * self._pointSet1.shape[0]/self._pointSet2.shape[0]

      
      tmp = timer()
      total = tmp - start
      outsideloop = tmp - start
      s2 = timer()

      tiledJPoints = []
      numIPoints = self._pointSet1.shape[0]
      for jPoint in self._pointSet2:
        tiledJPoints.append(np.tile(jPoint, (numIPoints, 1)))

      
      numJPoints = self._pointSet2.shape[0]
      numerators = np.zeros((numIPoints, numJPoints))
      denominators = np.zeros((numIPoints, numJPoints))
      
      e2 = timer()
      s = timer()
      for i in range(numIPoints):
        for j, jPoint in enumerate(self._pointSet2):
          sjTmiDiff = jPoint - transformedPointSet1[i]
          numerators[i,j] = np.exp(constant1 * np.dot(sjTmiDiff, sjTmiDiff))

          jPoints = tiledJPoints[j]
          sjTmkDiffs = jPoints - transformedPointSet1
          diffSquares = inner1d(sjTmkDiffs, sjTmkDiffs)
          exponents = constant1 * diffSquares
          termsInDenominatorSum = np.exp(exponents)
          denominatorSum = np.sum(termsInDenominatorSum)
          denominators[i,j] = denominatorSum

      
      e = timer()
      total += e - s
      denominators += constant2
      P = numerators / denominators


      print "Normalized sum(P):", np.sum(np.sum(P))/(numIPoints*numJPoints)
      print "MeanMax(P,0)", np.mean(np.max(P,axis=0))
      print "MeanMax(P,1)", np.mean(np.max(P,axis=1))
      print "MedianMax(P,0)", np.median(np.max(P,axis=0))
      print "MedianMax(P,1)", np.median(np.max(P,axis=1))
      

      end = timer()
      print "loop:", end-start
      print "inner loop:", total 
      print "outsideloop:", e2-s2
      theta, sigmaSquare = self._solveRigid(P)
      #registered = True
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

def addEdgesToImage(image, edges, colorIx):
  for row, col in zip(edges[0], edges[1]):
    image[row, col, colorIx] = 255

def addNdArrayPointsToImage(image, points, colorIx):
  for point in points:
    row = int(point[0])
    col = int(point[1])
    image[row, col, colorIx] = 255

def computeSquareDistance(point1, point2):
  diff = point1 - point2
  return float(diff[0]**2 + diff[1]**2)

def computeSquareDistances(points1, points2):
  numPoints1 = points1.shape[0]
  numPoints2 = points2.shape[0]

  squareDistances = np.zeros((numPoints1, numPoints2))
  for i, point1 in enumerate(points1):
    for j, point2 in enumerate(points2):
      squareDistances[i,j] = computeSquareDistance(point1, point2)
  return squareDistances

def comuteClosestNeighborLikeness(points1, points2):
  squareDistances = computeSquareDistances(points1, points2)
  from1ClosestNeighbor = np.min(squareDistances, axis=1)
  from2ClosestNeighbor = np.min(squareDistances, axis=0)
  return np.mean(from1ClosestNeighbor) + np.mean(from2ClosestNeighbor)

if __name__ == "__main__":
  filePath1 = "images/early_tests_white/4_01.jpg"
  filePath2 = "images/early_tests_white/6_01.jpg"

  img1 = misc.imread(filePath1)
  edgeDetector1 = EdgeDetector(img1)

  img2 = misc.imread(filePath2)
  edgeDetector2 = EdgeDetector(img2)

  sigma = 2
  thresholdFactor = 8.0
  radius = 30

  edges1 = edgeDetector1.getEdges(sigma, thresholdFactor, radius)
  edges2 = edgeDetector2.getEdges(sigma, thresholdFactor, radius)

  
  points1 = np.zeros((len(edges1[0]), 2))
  for ix in range(len(edges1[0])):
    points1[ix, 0] = edges1[0][ix]
    points1[ix, 1] = edges1[1][ix]
  print points1.shape
  points1 = points1[::2,:]
  print points1.shape

  points2 = np.zeros((len(edges2[0]), 2))
  for ix in range(len(edges2[0])):
    points2[ix, 0] = edges2[0][ix]
    points2[ix, 1] = edges2[1][ix]
  print points2.shape
  points2 = points2[::2,:]
  print points2.shape
  

  '''
  |
  |
  2   2
  |\ / 
  | X
  |/ \ 
  1---1------------------
  '''
  '''
  points1 = np.zeros((2,2))
  points1[1,:] = [1.0, 0.0]

  points2 = np.zeros((2,2))
  points2[0,:] = [0, 1.0]
  points2[0,:] = [1.0, 1.0]
  '''

  matcher = CoherentPointDriftMatcher2D(points1, points2)
  start = timer()
  scale, rotation, translation = matcher.match(0.0)
  end = timer()
  print "matcher.match:", end-start
  
  #print "target", points2
  #print "before transform", points1
  transformed = transform(scale, rotation, translation, points1)
  #print "after transform", transformed

  print "Closest neighbor likeness:", comuteClosestNeighborLikeness(points2, transformed)


  #addEdgesToImage(img1, edges1, 0)
  #addEdgesToImage(img2, edges2, 0)
  
  #print points1
  addNdArrayPointsToImage(img1, points1, 0)
  addNdArrayPointsToImage(img2, points1, 0)
  addNdArrayPointsToImage(img1, points2, 0)
  addNdArrayPointsToImage(img2, points2, 0)
  
  #addNdArrayPointsToImage(img2, points1, 2)
  #addNdArrayPointsToImage(img1, points2, 2)
  #addNdArrayPointsToImage(img2, points2, 2)
  addNdArrayPointsToImage(img1, transformed, 1)
  addNdArrayPointsToImage(img2, transformed, 1)

  plt.figure()
  plt.imshow(img1)

  plt.figure()
  plt.imshow(img2)
 
