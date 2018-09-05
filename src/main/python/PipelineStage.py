import ImageUtilities
from EdgeDetector import EdgeDetector
import numpy as np
import PointCloud


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
        return PointCloud.PointCloudToRgbImage(self._executionResult, 0)

    def __ne__(self, other):
        if type(self) != type(other):
            return True
        if self._sigma != other._sigma:
            return True
        if self._threshold != other._threshold:
            return True


class CropStage:
    def __init__(self, x, y, width, height):
        self._x = x
        self._y = y
        self._width = width
        self._height = height
        self._executionResult = None

    def execute(self, rgbMatrix):
        shape = rgbMatrix.shape
        if (len(shape) != 3 or shape[2] != 3):
            raise Exception("Input to CropStage must be rgb matrix.")

        intX = int((self._x - self._width * 0.5) * shape[1])
        intY = int((self._y - self._height * 0.5) * shape[0])
        intWidth = int(self._width * shape[1])
        intHeight = int(self._height * shape[0])

        print(intX, intY, intWidth, intHeight)

        self._executionResult = rgbMatrix[intY:intY + intHeight,
                                          intX:intX + intWidth,
                                          :]
        return self._executionResult

    def getImageRepresentation(self):
        return self._executionResult

    def __ne__(self, other):
        if type(self) != type(other):
            return True

        return (self._x != other._x or
                self._y != other._y or
                self._width != other._width or
                self._height != other._height)
