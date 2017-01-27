from scipy import misc
import matplotlib.pyplot as plt
import math
from ImageUtilities import addPointsToImage
from EdgeDetector import EdgeDetector

class ReferenceImage:
    def __init__(self, path, comment):
        self.comment = comment
        self.image = misc.imread(path)

class ConfigCreator:
    def __init__(self):
        self._referenceImages = []
        self._referenceImagesFigure = plt.figure()

        self._sigma = 2.0
        self._thresholdFactor = 8.0
        self._radius = 30.0
        self._keepFactor = 1.0
        
    def readImages(self):
        inputStr = raw_input("Path to image (leave empty when done): ")
        while inputStr:
            filePath = inputStr
            comment = raw_input("Comment: ")
            self._referenceImages.append(ReferenceImage(filePath, comment))
            inputStr = raw_input("Path to image (leave empty when done): ")

        print "Read " + str(len(self._referenceImages)) + " images."

    def calibrateEdgeDetection(self):
        self._drawReferenceImages()
        
        while True:
            print "Current parameters:"
            self._printIndentedParameters()
            inputStr = raw_input("Which parameter? ")
            if not self._tryUpdateParameter(inputStr):
                break
            self._drawReferenceImages()
            
        print "Final parameters:"
        self._printIndentedParameters()

    def _printIndentedParameters(self):
        print "  0 sigma:", self._sigma
        print "  1 thresholdFactor:", self._thresholdFactor
        print "  2 radius:", self._radius
        print "  3 keepFactor:", self._keepFactor

    def _tryUpdateParameter(self, inputStr):
        if not inputStr:
            return False

        try:
            parameterAsInt = int(inputStr)
        except e:
            print "Exception raised while parsing string."
            return False

        if parameterAsInt < 0 or parameterAsInt > 3:
            return False

        valueStr = raw_input("New value: ")
        try:
            valueAsFloat = float(valueStr)
        except e:
            print "Exception raised while parsing string."
            return False

        if parameterAsInt == 0:
            self._sigma = valueAsFloat
        if parameterAsInt == 1:
            self._thresholdFactor = valueAsFloat
        if parameterAsInt == 2:
            self._radius = valueAsFloat
        if parameterAsInt == 3:
            self._keepFactor = valueAsFloat

        return True

    
    def _drawReferenceImages(self):
        numPlotsPerSide = int(math.ceil(math.sqrt(len(self._referenceImages))))
        print "numPlotsPerSide:", numPlotsPerSide
        for ix, reference in enumerate(self._referenceImages):
            ax = self._referenceImagesFigure.add_subplot(numPlotsPerSide, numPlotsPerSide, ix + 1)

            edgeDetector = EdgeDetector(reference.image)
            points = edgeDetector.getEdgesAsPoints(self._sigma, self._thresholdFactor, self._radius)
            imageToShow = reference.image.copy()
            addPointsToImage(imageToShow, points, 1)
            
            ax.imshow(imageToShow)
            
        plt.show(block=False)
        
