class NopStage:
    def __init__(self):
        self._image = None

    def exectute(self, inData):
        self._image = inData
        return inData

    def getImageRepresentation(self):
        return self._image

    def __ne__(self, other):
        if type(self) != type(other):
            return True
        return False


class EdgeDetectorStage:
    def __init__(self, sigma, threshold):
        self._sigma = sigma
        self._threshold = threshold
        self._resultData = None

    def execute(self, inData):
        return inData

    def getImageRepresentation(self):
        return None

    def __ne__(self, other):
        if type(self) != type(other):
            return True
        if self._sigma != other._sigma:
            return True
        if self._threshold != other._threshold:
            return True
