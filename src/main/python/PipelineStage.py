import ImageUtilities
from EdgeDetector import EdgeDetector
import numpy as np
from PointCloud import PointCloud, PointCloudToRgbImage
from PointCloudHandler import getPointCloudFromIterable
from SimulatedAnnealingPointMatcher2D import SimulatedAnnealingPointMatcher2D
from MeanShortestDistanceFitnessComputer import MeanShortestDistanceFitnessComputer
from MostPopulatedCircleFinder import MostPopulatedCircleFinder
import sys
from PIL import Image, ImageDraw


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
        self._executionResult = None

    def execute(self, inData):
        print("Executing edge detector stage")
        edgeDetector = EdgeDetector(inData)
        self._executionResult = edgeDetector.getEdges(self._sigma,
                                                      self._threshold)
        return self._executionResult

    def getImageRepresentation(self):
        return PointCloudToRgbImage(self._executionResult, 0)

    def __ne__(self, other):
        if type(self) != type(other):
            return True
        if self._sigma != other._sigma:
            return True
        if self._threshold != other._threshold:
            return True
        return False


class KeepInsideRadiusStage:
    def __init__(self, radius):
        self._radius = radius
        self._executionResult = None

    def execute(self, pointCloud):
        mean = pointCloud.mean()
        self._executionResult = PointCloud()
        radiusSquare = self._radius**2
        for x, y in pointCloud:
            squareDistanceFromMean = float((x - mean[0])**2 + (y - mean[1])**2)
            if squareDistanceFromMean <= radiusSquare:
                self._executionResult.addXY(float(x), float(y))
        return self._executionResult

    def getImageRepresentation(self):
        return PointCloudToRgbImage(self._executionResult, 0)

    def __ne__(self, other):
        if type(self) != type(other):
            return True
        return self._radius != other._radius


class MostPopulatedCircleStage:
    def __init__(self, radius):
        self._radius = radius
        self._executionResult = None

    def execute(self, pointCloud):
        mostPopulatedCircleFinder = MostPopulatedCircleFinder(pointCloud.asNumpyArray())
        center = mostPopulatedCircleFinder.get(self._radius)
        squareRadius = self._radius ** 2
        self._executionResult = PointCloud()
        for point in pointCloud:
            diff = point - center
            normSquare = diff[0]**2 + diff[1]**2
            if normSquare <= squareRadius:
                self._executionResult.addPoint(point)
        return self._executionResult

    def getImageRepresentation(self):
        return PointCloudToRgbImage(self._executionResult, 0)

    def __ne__(self, other):
        if type(self) != type(other):
            return True
        return self._radius != other._radius


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


class SimulatedAnnealingPointMatcherStage:
    def __init__(self, pointClouds, annealerSettings):
        self._annealers = {}
        self._fitnessComputers = {}
        self._referenceClouds = {}
        for pointCloud in pointClouds:
            jsonPath = pointCloud["filepath"]
            referenceName = pointCloud["name"]
            print(referenceName, jsonPath)

            with open(jsonPath) as f:
                referenceCloud = getPointCloudFromIterable(f)

            center = referenceCloud.mean()
            centeredReference = np.array(referenceCloud.asNumpyArray(), copy=True)
            centeredReference[:, 0] -= center[0]
            centeredReference[:, 1] -= center[1]

            fitnessComputer = MeanShortestDistanceFitnessComputer(centeredReference)
            annealer = SimulatedAnnealingPointMatcher2D(fitnessComputer)
            for name, setting in annealerSettings.items():
                if name == "NumIterations":
                    annealer.setNumIterations(int(setting))
                elif name == "StartTemperature":
                    annealer.setStartTemperature(float(setting))
                elif name == "InitialRotationSigma":
                    annealer.setInitialRotationSigma(float(setting))
                elif name == "SlowRotationSigma":
                    annealer.setSlowRotationSigma(float(setting))
                elif name == "InitialTranslationSigma":
                    annealer.setInitialTranslationSigma(float(setting))
                elif name == "SlowTranslationSigma":
                    annealer.setSlowTranslationSigma(float(setting))
                elif name == "SlowMovementBreakpoint":
                    annealer.setSlowMovementBreakpoint(float(setting))
                elif name == "Verbose":
                    annealer.setVerbose(bool(setting))
                else:
                    print("Unknown setting {}: {}".format(name, setting))

            # TODO: fix lifetime issues here so that we dont need to explicitly keep
            # fitnessComputer around.
            self._annealers[referenceName] = annealer
            self._fitnessComputers[referenceName] = fitnessComputer
            self._referenceClouds[referenceName] = centeredReference

    def execute(self, pointCloud):
        center = pointCloud.mean()
        centeredSample = np.array(pointCloud.asNumpyArray(), copy=True)
        centeredSample[:, 0] -= center[0]
        centeredSample[:, 1] -= center[1]

        self._bestReferenceName = "none"
        bestFitness = sys.float_info.max
        for referenceName, annealer in self._annealers.items():
            annealer.clearPoints()
            for point in centeredSample:
                annealer.addPoint(point[0], point[1])
            scale, rotation, translation, fitness = annealer.match()
            if (scale < 1.2 and scale > 0.8):
                if fitness < bestFitness:
                    bestFitness = fitness
                    self._bestReferenceName = referenceName
            print("referenceName: {}".format(referenceName))
            print("matched. bestFitness: {}".format(fitness))
            print("               scale: {}".format(scale))
            print("         translation: {}".format(translation))
            print("            rotation: {}".format(rotation))
            self._transformation = (scale, rotation, translation)
            self._lastCloud = centeredSample
        return self._bestReferenceName

    def getImageRepresentation(self):
        print("getImageRepresentation:", self._bestReferenceName)
        text = self._bestReferenceName
        size = 100
        canvas = Image.new("RGB", [size, size], (255, 255, 255))
        draw = ImageDraw.Draw(canvas)
        textWidth, textHeight = draw.textsize(text)
        offset = (5, 5)
        white = "#000000"
        draw.text(offset, text, fill=white)
        ret = 255.0 - np.asarray(canvas)

        middleOfImage = np.array([[50.0, 50.0]])

        cloudPoints = np.dot(self._lastCloud, self._transformation[1]) + self._transformation[2] + middleOfImage

        referencePoints = self._referenceClouds[self._bestReferenceName] + middleOfImage

        ImageUtilities.addPointsToImage(ret, cloudPoints, 0)
        ImageUtilities.addPointsToImage(ret, referencePoints, 1)

        return ret

    def __ne__(self, other):
        if type(self) != type(other):
            return True

        # TODO: dont do pointer comparison here.
        return self._annealers != other._annealers
