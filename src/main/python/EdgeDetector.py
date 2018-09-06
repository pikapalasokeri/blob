from scipy import ndimage
import numpy as np
from PointCloud import PointCloud


class EdgeDetector:
    def __init__(self, monochromeImage):
        imageShape = monochromeImage.shape
        if len(imageShape) != 2:
            raise Exception("Image must be monochrome.")

        self._image = monochromeImage

    def getEdges(self, scale, thresholdFactor):
        laplacianOfGaussian = ndimage.gaussian_laplace(self._image, scale)  # ish 0.57 seconds
        zeroCrossings = _findZeroCrossings(laplacianOfGaussian, thresholdFactor)  # ish 0.25 sec
        result = PointCloud()
        for x, y in zip(zeroCrossings[0], zeroCrossings[1]):
            result.addXY(float(x), float(y))
        return result


def _findZeroCrossings(image, thresholdFactor):
    if image.shape == (0, 0):
        threshold = 0.0
    else:
        threshold = np.mean(np.absolute(image)) * thresholdFactor

    sign = np.sign(image)

    rightSignDiff = sign[:, :-1] - sign[:, 1:]
    rightDiff = np.abs(image[:, :-1] - image[:, 1:])
    rightCrossings = np.nonzero((rightSignDiff != 0.0) & (rightDiff > threshold))

    downSignDiff = sign[:-1, :] - sign[1:, :]
    downDiff = np.abs(image[:-1, :] - image[1:, :])
    downCrossings = np.nonzero((downSignDiff != 0.0) & (downDiff > threshold))

    return (np.concatenate((rightCrossings[0] + 0.5, downCrossings[0])), np.concatenate((rightCrossings[1], downCrossings[1] + 0.5)))
