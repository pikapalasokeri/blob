class NopStage:
    def __init__(self):
        self._image = None

    def exectute(self, inData):
        self._image = inData
        return inData

    def getImageRepresentation(self):
        return self._image


class EdgeDetectorStage:
    def __init__(self, sigma, threshold):
        self._sigma = sigma
        self._threshold = threshold
        self._resultData = None

    def execute(self, inData):
        return inData

    def getImageRepresentation(self):
        return None
