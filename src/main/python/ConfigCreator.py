import matplotlib.pyplot as plt
import math
import os
from ImageUtilities import addPointsToImage, rgb2grayNaive
from EdgeDetector import EdgeDetector
from DirectoryImageReader import DirectoryImageReader
import PointCloudHandler

sigmaNumber = 1
thresholdFactorNumber = 2
radiusNumber = 3
keepFactorNumber = 4
dumpToFileNumber = 9
exitNumber = 0


class ConfigCreator:
    def __init__(self, imageSupplier):
        self._imageSupplier = imageSupplier

        self._referenceImages = []
        self._referenceImagesFigure = plt.figure()

        self._sigma = 2.0
        self._thresholdFactor = 2.0
        self._radius = 40.0
        self._keepFactor = 1.0

    def readImages(self):
        self._referenceImages.extend(self._imageSupplier.generate())
        print("Read " + str(len(self._referenceImages)) + " images.")

    def calibrateEdgeDetection(self):
        self._drawReferenceImages()

        while True:
            print("Current parameters:")
            self._printIndentedParameters()
            inputStr = input("Which parameter? ")
            if not self._tryUpdateParameter(inputStr):
                break
            self._drawReferenceImages()

        print("Final parameters:")
        self._printIndentedParameters()

    def _printIndentedParameters(self):
        print("  " + str(sigmaNumber) + " sigma:", self._sigma)
        print("  " + str(thresholdFactorNumber) + " thresholdFactor:", self._thresholdFactor)
        print("  " + str(radiusNumber) + " radius:", self._radius)
        print("  " + str(keepFactorNumber) + " keepFactor:", self._keepFactor)
        print("  " + str(dumpToFileNumber) + " dump point clouds to file")
        print("  " + str(exitNumber) + " exit")

    def _tryUpdateParameter(self, inputStr):
        if not inputStr:
            return False

        try:
            parameterAsInt = int(inputStr)
        except:
            print("Exception raised while parsing string.")
            return False

        if parameterAsInt == exitNumber:
            return False
        if parameterAsInt == dumpToFileNumber:
            self._dumpPointsToFile()
            return True

        valueStr = input("New value: ")
        try:
            valueAsFloat = float(valueStr)
        except:
            print("Exception raised while parsing string.")
            return False

        if parameterAsInt == sigmaNumber:
            self._sigma = valueAsFloat
        if parameterAsInt == thresholdFactorNumber:
            self._thresholdFactor = valueAsFloat
        if parameterAsInt == radiusNumber:
            self._radius = valueAsFloat
        if parameterAsInt == keepFactorNumber:
            self._keepFactor = valueAsFloat

        return True

    def _drawReferenceImages(self):
        numPlotsPerSide = int(math.ceil(math.sqrt(len(self._referenceImages))))
        print("numPlotsPerSide:", numPlotsPerSide)
        for ix, reference in enumerate(self._referenceImages):
            ax = self._referenceImagesFigure.add_subplot(numPlotsPerSide, numPlotsPerSide, ix + 1)

            edgeDetector = EdgeDetector(rgb2grayNaive(reference.image))
            edges = edgeDetector.getEdges(self._sigma, self._thresholdFactor, self._radius)
            imageToShow = reference.image.copy()
            addPointsToImage(imageToShow, edges, 1)

            ax.imshow(imageToShow)

        plt.show(block=False)

    def _dumpPointsToFile(self):
        inputDirStr = _userCheckedInput("Image dir path: ")
        outputDirStr = _userCheckedInput("Output dir path: ")
        outputPostfixStr = _userCheckedInput("Output postfix str: ")

        imageReader = DirectoryImageReader(inputDirStr)
        for image in imageReader.generate():
            print(image.comment)
            edgeDetector = EdgeDetector(rgb2grayNaive(image.image))
            cloud = edgeDetector.getEdges(self._sigma, self._thresholdFactor, self._radius)

            outFilePath = os.path.join(outputDirStr, image.comment + outputPostfixStr)
            outFile = open(outFilePath, "w")
            PointCloudHandler.savePointCloudToWriteable(cloud, outFile)
            outFile.close()


def _userCheckedInput(displayString):
    inputStr = input(displayString)
    while True:
        if input("Correct? (y/n) ") == "y":
            break
        inputStr = input(displayString)
    return inputStr
