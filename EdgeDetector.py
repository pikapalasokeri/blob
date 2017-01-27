from scipy import ndimage
import numpy as np
import matplotlib.pyplot as plt
import ImageUtilities

class EdgeDetector:
  def __init__(self, image, logLevel = None):
    imageShape = image.shape
    if len(imageShape) != 3:
      raise Exception("Image must be RGB.")
    if imageShape[2] != 3:
      raise Exception("Image must be RGB.")

    self._image = image
    self._logLevel = logLevel
    self._oneDImage = ImageUtilities.rgb2grayNaive(self._image)
    
  def getEdges(self, scale, thresholdFactor, radius):
    laplacianOfGaussian = ndimage.gaussian_laplace(self._oneDImage, scale) # ish 0.57 seconds
    zeroCrossings = _findZeroCrossings(laplacianOfGaussian, thresholdFactor) # ish 0.25 sec
    return _keepInsideRadius(zeroCrossings, radius) # ish 0.05 secs

  def getEdgesAsPoints(self, scale, thresholdFactor, radius):
    edges = self.getEdges(scale, thresholdFactor, radius)
    points = np.zeros((len(edges[0]), 2))
    for ix in range(len(edges[0])):
      points[ix, 0] = edges[0][ix]
      points[ix, 1] = edges[1][ix]
    return points

def _findZeroCrossings(oneDImage, thresholdFactor):
  threshold = np.mean(np.absolute(oneDImage))*thresholdFactor
  zeroCrossings = []

  sign = np.sign(oneDImage)

  rightSignDiff = sign[:,:-1] - sign[:,1:]
  rightDiff = np.abs(oneDImage[:,:-1] - oneDImage[:,1:])
  rightCrossings = np.nonzero((rightSignDiff != 0.0) & (rightDiff > threshold))
  zeroCrossings = rightCrossings
  
  downSignDiff = sign[:-1,:] - sign[1:,:]
  downDiff = np.abs(oneDImage[:-1,:] - oneDImage[1:,:])
  downCrossings = np.nonzero((downSignDiff != 0.0) & (downDiff > threshold))

  return (np.concatenate((rightCrossings[0], downCrossings[0])), np.concatenate((rightCrossings[1], downCrossings[1])))

def _keepInsideRadius(points, radius):
  xMean = np.mean(points[0])
  yMean = np.mean(points[1])

  result = []
  radiusSquare = radius**2
  for x, y in zip(points[0], points[1]):
    squareDistanceFromMean = float((x-xMean)**2 + (y-yMean)**2)
    if squareDistanceFromMean <= radiusSquare:
      result.append((x,y))

  numPoints = len(result)
  resultX = np.zeros((numPoints, 1))
  resultY = np.zeros((numPoints, 1))
  for i, point in enumerate(result):
    resultX[i] = point[0]
    resultY[i] = point[1]
  
  return resultX, resultY
