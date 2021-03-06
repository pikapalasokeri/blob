from PyQt5.QtCore import QObject, pyqtSignal
from ImageProcessingPipeline import ImageProcessingPipeline
from BruteForceMatcherStage import BruteForceMatcherStage
from FractionPointRemoverStage import FractionPointRemoverStage
import PipelineStage
import json

RAW_IMAGE_STAGE = "Raw image"


class JsonPipelineKeeper(QObject):
    processingModelUpdated = pyqtSignal(ImageProcessingPipeline)

    def __init__(self):
        super().__init__()

    def tryUpdate(self, maybeJsonText):
        try:
            validJson = json.loads(maybeJsonText)
            if type(validJson) == list:
                nodeNames = []
                for element in validJson:
                    if "name" in element:
                        nodeNames.append(element["name"])
                self.processingModelUpdated.emit(jsonToPipeline(validJson))
        except json.JSONDecodeError as e:
            print(str(e))


def jsonToPipeline(jsonDict):
    pipeline = ImageProcessingPipeline()
    pipeline.appendStage(PipelineStage.NopStage(), RAW_IMAGE_STAGE)

    for element in jsonDict:
        name = element["name"]
        stageType = element["type"]
        if stageType == "Crop":
            pipeline.appendStage(PipelineStage.CropStage(element["x"],
                                                         element["y"],
                                                         element["width"],
                                                         element["height"]),
                                 name)
        elif stageType == "GrayscaleConversion":
            pipeline.appendStage(PipelineStage.GrayscaleConversionStage(), name)
        elif stageType == "EdgeDetector":
            pipeline.appendStage(PipelineStage.EdgeDetectorStage(element["sigma"],
                                                                 element["threshold"]),
                                 name)
        elif stageType == "KeepInsideRadius":
            pipeline.appendStage(PipelineStage.KeepInsideRadiusStage(element["radius"]),
                                 name)
        elif stageType == "MostPopulatedCircle":
            pipeline.appendStage(PipelineStage.MostPopulatedCircleStage(element["radius"]),
                                 name)
        elif stageType == "SimulatedAnnealing":
            pipeline.appendStage(PipelineStage.SimulatedAnnealingPointMatcherStage(element["reference_pointclouds"],
                                                                                   element["annealer_settings"]),
                                 name)
        elif stageType == "BruteForceMatcher":
            pipeline.appendStage(BruteForceMatcherStage(element["reference_pointclouds"],
                                                        element["matcher_settings"]),
                                 name)
        elif stageType == "FractionPointRemover":
            pipeline.appendStage(FractionPointRemoverStage(element["keep_fraction"]),
                                 name)
        elif stageType == "Nop":
            pipeline.appendStage(PipelineStage.NopStage(), name)
        else:
            raise Exception("Unknown pipeline stage type '{}'".format(stageType))
    return pipeline
