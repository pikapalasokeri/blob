from PointCloud import PointCloud, PointCloudToRgbImage


class FractionPointRemoverStage:
    def __init__(self, keepFraction):
        self._keepFraction = keepFraction

    def execute(self, pointCloud):
        print("Executing fraction point remover stage")
        '''
        I really don't know why this method works so well, except for threshold 0.8 or 0.2,
        but I'm keeping it since it seems to work very well for everything else,
        and 0.8 and 0.2 are off by 2 at most.
        '''
        newCloud = PointCloud()

        keepThreshold = self._keepFraction
        accumulatedKeep = 0.0
        accumulatedKeepCorrection = 0.0
        for point in pointCloud:
            if accumulatedKeep - accumulatedKeepCorrection < keepThreshold:
                newCloud.addPoint(point)
            accumulatedKeep += keepThreshold

            if accumulatedKeep - accumulatedKeepCorrection >= 1.0:
                accumulatedKeepCorrection += 1.0

        self._executionResult = newCloud
        return self._executionResult

    def getImageRepresentation(self):
        return PointCloudToRgbImage(self._executionResult, 0)

    def __ne__(self, other):
        if type(self) != type(other):
            return True

        # TODO: dont do pointer comparison here.
        return self._matchers != self._matchers
