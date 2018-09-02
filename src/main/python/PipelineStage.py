import ImageUtilities
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
    def __init__(self, sigma, threshold):
        self._sigma = sigma
        self._threshold = threshold
        self._resultData = None

    def execute(self, inData):
        print("Executing edge detector stage")
        return inData

    def getImageRepresentation(self):
        print("Getting edge detection image representation")
        return None

    def __ne__(self, other):
        if type(self) != type(other):
            return True
        if self._sigma != other._sigma:
            return True
        if self._threshold != other._threshold:
            return True
