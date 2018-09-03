import ImageUtilities
from EdgeDetector import EdgeDetector
import numpy as np


class NopStage:
    def __init__(self):
        self._image = None

    def execute(self, inData):
        print("Executing nop stage")
        self._image = inData
        return inData

    def getImageRepresentation(self):
        print("Getting nop image representation")
        return self._image

    def __ne__(self, other):
        if type(self) != type(other):
            return True
        return False


class GrayscaleConversionStage:
    def __init__(self):
        self._grayMatrix = None

    def execute(self, inData):
        print("Executing grayscale convertion stage")
        self._grayMatrix = ImageUtilities.rgb2grayNaive(inData)
        return self._grayMatrix

    def getImageRepresentation(self):
        shape = self._grayMatrix.shape
        ret = np.zeros((shape[0], shape[1], 3))
        ret[..., 0] = self._grayMatrix
        ret[..., 1] = self._grayMatrix
        ret[..., 2] = self._grayMatrix
        return ret


class EdgeDetectorStage:
    def __init__(self, sigma, threshold, radius):
        self._sigma = sigma
        self._threshold = threshold
        self._radius = radius
        self._executionResult = None

    def execute(self, inData):
        print("Executing edge detector stage")
        edgeDetector = EdgeDetector(inData)
        self._executionResult = edgeDetector.getEdges(self._sigma,
                                                      self._threshold,
                                                      self._radius)
        return self._executionResult

    def getImageRepresentation(self):
        cols = int(self._executionResult.max()[1] + self._executionResult.min()[1]) + 1
        rows = int(self._executionResult.max()[0] + self._executionResult.min()[0]) + 1
        print(cols, rows)
        ret = np.zeros((rows, cols, 3))
        ImageUtilities.addPointsToImage(ret, self._executionResult, 0)
        return ret

    def __ne__(self, other):
        if type(self) != type(other):
            return True
        if self._sigma != other._sigma:
            return True
        if self._threshold != other._threshold:
            return True
