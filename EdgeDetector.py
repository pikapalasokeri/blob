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
    
  def getEdges(self, scale, thresholdFactor):
    laplacianOfGaussian = ndimage.gaussian_laplace(self._oneDImage, scale)
    return _findZeroCrossings(laplacianOfGaussian, thresholdFactor)

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
