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
      print ix
      ix += 1

      sigmaSquareChange = oldSigmaSquare - sigmaSquare
      oldSigmaSquare = sigmaSquare
      print "Change in sigmaSquare:", sigmaSquareChange
      if ix == 250 or sigmaSquare < 0.0 or sigmaSquareChange < 0.001:
        return theta[0], theta[1], theta[2]
      transformedPointSet1 = transform(theta[0], theta[1], theta[2], self._pointSet1)
      print "scale:", theta[0]
      print "rotation:", theta[1]
      print "translation:", theta[2]
      print "sigmaSquare:", sigmaSquare
      #print self._pointSet1
      #print transformedPointSet1


      start = timer()
      tmp = timer()
      total = tmp - start
      for i, iPoint in enumerate(self._pointSet1):
        for j, jPoint in enumerate(self._pointSet2):
          sjTmiDiff = jPoint - transformedPointSet1[i]
          numerator = np.exp(-1.0/(2.0*sigmaSquare) * np.dot(sjTmiDiff, sjTmiDiff))

          s = timer()
          denominatorSum = 0.0

          numIPoints = self._pointSet1.shape[0]

          jPoints = np.tile(jPoint, (numIPoints, 1))
          sjTmkDiffs = jPoints - transformedPointSet1
          diffSquares = inner1d(sjTmkDiffs, sjTmkDiffs)
          exponents = -1.0/(2.0*sigmaSquare) * diffSquares
          termInDenominatorSum = np.exp(exponents)
          denominatorSum = np.sum(termInDenominatorSum)
          denominator = denominatorSum + (2.0*np.pi*sigmaSquare) * w / (1 - w) * self._pointSet1.shape[0]/self._pointSet2.shape[0]

          e = timer()
          total += e - s

          #print "P[i,j]", numerator, denominator, denominatorSum, numerator/denominator
          P[i,j] = numerator / denominator
          #print i, j, P[i,j]
      end = timer()
      print "loop:", end-start
      print "inner loop:", total 
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

    #print "M", M
    #print "S", S

    NP = np.dot(np.dot(np.ones((1, P.shape[0])), P), np.ones((P.shape[1], 1))) # Sum of all elements in P matrix
    muS = 1.0/(NP) * np.dot(S.transpose(), np.dot(P.transpose(), np.ones((P.shape[0], 1)))) # (2,1) "mean" vector
    muM = 1.0/(NP) * np.dot(M.transpose(), np.dot(P, np.ones((P.shape[1], 1))))             # (2,1) "mean" vector

    #print "NP:", NP
    #print "muS:", muS
    #print "muM:", muM

    Shat = S - muS.transpose()
    Mhat = M - muM.transpose()

    #print "Shat", Shat
    #print "Mhat", Mhat

    A = np.dot(np.dot(Shat.transpose(), P.transpose()), Mhat)

    #print "A", A

    U, shapeSigma, Vt = np.linalg.svd(A)
    #you are here. something is fishy. scale shrinks but doesnt expand again. sigmaSquare goes to 0 (or -0)
    C = np.eye(2)
    C[-1:-1] = np.linalg.det(np.dot(U, Vt))
    #print "C", C
    R = np.dot(U, np.dot(C, Vt))

    diag = np.diag(np.squeeze(np.dot(P, np.ones((P.shape[1], 1)))))
    #print diag
    #print "num:", np.trace(np.dot(A.transpose(), R))
    #print "den:", np.trace(np.dot(Mhat.transpose(), np.dot(diag, Mhat)))
    a = np.trace(np.dot(A.transpose(), R)) / np.trace(np.dot(Mhat.transpose(), np.dot(diag, Mhat)))
    #a = 1.0
    t = (muS - a*np.dot(R, muM)).transpose()
    #print "t", t

    diag = np.diag(np.squeeze(np.dot(P.transpose(), np.ones((P.shape[0], 1)))))
    print np.trace(np.dot(Shat.transpose(), np.dot(diag, Shat)))
    print a * np.trace(np.dot(A.transpose(), R))
    sigmaSquare = 1.0/(2.0*NP) * (np.trace(np.dot(Shat.transpose(), np.dot(diag, Shat))) - a * np.trace(np.dot(A.transpose(), R)))
    
    end = timer()
    print "one iteration _solveRigid:", end-start
    return (a, R, t), sigmaSquare

def transform(scale, rotation, translation, points):
  return scale*np.dot(points, rotation.transpose()) + translation




def computeDistances(points):
  result = []

  dimX = points[0]
  dimY = points[1]
  numPoints = len(dimX)
  for ix1 in range(0, numPoints):
    x1 = dimX[ix1]
    y1 = dimY[ix1]
    for ix2 in range(ix1+1, numPoints):
      x2 = dimX[ix2]
      y2 = dimY[ix2]
      distance = np.sqrt((x1-x2)**2 + (y1-y2)**2)
      result.append(distance)

  return result

def addEdgesToImage(image, edges, colorIx):
  for row, col in zip(edges[0], edges[1]):
    image[row, col, colorIx] = 255

def addNdArrayPointsToImage(image, points, colorIx):
  for point in points:
    row = int(point[0])
    col = int(point[1])
    image[row, col, colorIx] = 255

def computeMatchMeasure(edges1, edges2):
  distances1 = computeDistances(edges1)
  distances2 = computeDistances(edges2)
  return 0.0

if __name__ == "__main__":
  filePath1 = "images/early_tests/4_03.jpg"
  filePath2 = "images/early_tests/4_04.jpg"

  img1 = misc.imread(filePath1)
  edgeDetector1 = EdgeDetector(img1)

  img2 = misc.imread(filePath2)
  edgeDetector2 = EdgeDetector(img2)

  sigma = 4
  thresholdFactor = 8.0
  
  edges1 = edgeDetector1.getEdges(sigma, thresholdFactor)
  edges2 = edgeDetector2.getEdges(sigma, thresholdFactor)

  
  points1 = np.zeros((len(edges1[0]), 2))
  for ix in range(len(edges1[0])):
    points1[ix, 0] = edges1[0][ix]
    points1[ix, 1] = edges1[1][ix]
  print points1.shape
  points1 = points1[::5,:]
  print points1.shape

  points2 = np.zeros((len(edges2[0]), 2))
  for ix in range(len(edges2[0])):
    points2[ix, 0] = edges2[0][ix]
    points2[ix, 1] = edges2[1][ix]
  print points2.shape
  points2 = points2[::5,:]
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
  scale, rotation, translation = matcher.match(0.001)
  end = timer()
  print "matcher.match:", end-start
  
  print "target", points2
  print "before transform", points1
  transformed = transform(scale, rotation, translation, points1)
  print "after transform", transformed

  #addEdgesToImage(img1, edges1, 0)
  #addEdgesToImage(img2, edges2, 0)
  
  print points1
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


  print len(edges1[0])

  dist1 = computeDistances(edges1)
  dist2 = computeDistances(edges2)

  plt.figure()
  plt.plot(sorted(dist1), 'b')
  plt.plot(sorted(dist2), '--r')
  plt.show()
  

  
