class ImageProcessingPipeline:
    def __init__(self):
        self._stages = []
        self._names = []

    def executeUntil(self, lastStageName, image):
        result = image
        lastStage = None
        for stage, name in self._stages:
            result = stage.execute(result)
            lastStage = stage
            if name == lastStageName:
                break
        return lastStage.getImageRepresentation()

    def appendStage(self, stage, name):
        print("appending state")
        print(stage)
        self._stages.append((stage, name))

    def getStageNames(self):
        return [name for (stage, name) in self._stages]
