class ImageProcessingPipeline:
    def __init__(self):
        self._stages = []
        self._names = []

    def __eq__(self, other):
        if other is None:
            return False

        if len(self._stages) != len(other._stages):
            return False

        for p, q in zip(self._stages, other._stages):
            if p[1] != q[1]:
                return False
            if p[0] != q[0]:
                return False

        return True

    def executeUntil(self, lastStageName, image):
        result = image
        lastStage = None
        for stage, name in self._stages:
            result = stage.execute(result)
            lastStage = stage
            if name == lastStageName:
                break
        return result, lastStage

    def executeUntilRaw(self, lastStageName, image):
        result, _ = self.executeUntil(lastStageName, image)
        return result

    def executeUntilImage(self, lastStageName, image):
        _, lastStage = self.executeUntil(lastStageName, image)
        return lastStage.getImageRepresentation()

    def appendStage(self, stage, name):
        self._stages.append((stage, name))

    def getStageNames(self):
        return [name for (stage, name) in self._stages]
