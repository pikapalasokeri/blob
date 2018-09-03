from PyQt5.QtWidgets import QWidget, QGridLayout, QPlainTextEdit, QListWidget
from PyQt5.QtCore import QObject, pyqtSignal
from ImageProcessingPipeline import ImageProcessingPipeline
import PipelineStage
import json


RAW_IMAGE_STAGE = "Raw image"


class JsonParser(QObject):
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
                self.processingModelUpdated.emit(self._jsonToPipeline(validJson))
        except json.JSONDecodeError as e:
            print(str(e))

    def _jsonToPipeline(self, jsonDict):
        pipeline = ImageProcessingPipeline()
        pipeline.appendStage(PipelineStage.NopStage(), RAW_IMAGE_STAGE)

        for element in jsonDict:
            name = element["name"]
            stageType = element["type"]
            if stageType == "GrayscaleConversion":
                pipeline.appendStage(PipelineStage.GrayscaleConversionStage(), name)
            elif stageType == "EdgeDetector":
                pipeline.appendStage(PipelineStage.EdgeDetectorStage(element["sigma"],
                                                                     element["threshold"],
                                                                     element["radius"]),
                                     name)
            elif stageType == "Nop":
                pipeline.appendStage(PipelineStage.NopStage(), name)
            else:
                raise Exception("Unknown pipeline stage type '{}'".format(stageType))

        return pipeline


class JsonTextEdit(QPlainTextEdit):
    newTextChanged = pyqtSignal(str)

    def __init__(self, text, parent):
        super().__init__(text, parent)
        self.textChanged.connect(self.newTextChangedProxy)

    def newTextChangedProxy(self):
        self.newTextChanged.emit(self.toPlainText())


class JsonEditorWidget(QWidget):
    def __init__(self, parent, jsonParser):
        super().__init__(parent)
        editor = JsonTextEdit('[\n'
                              '{\n'
                              '"name": "gray",\n'
                              '"type": "GrayscaleConversion"\n'
                              '},\n'
                              '{\n'
                              '"name": "edges",\n'
                              '"type": "EdgeDetector",\n'
                              '"sigma": 1.0,\n'
                              '"threshold": 1.0,\n'
                              '"radius": 50.0\n'
                              '},\n'
                              '{\n'
                              '"name": "stage2",\n'
                              '"type": "Nop"\n'
                              '}\n'
                              ']', self)
        editor.setStyleSheet("QPlainTextEdit{font-family: Courier New;}")
        editor.resize(400, 700)

        editor.newTextChanged.connect(jsonParser.tryUpdate)


class NodeListWidget(QWidget):
    def __init__(self, parent, imageTableModel):
        super().__init__(parent)
        self._nodeList = QListWidget(self)
        self._nodeList.resize(200, 400)
        self._nodeList.itemClicked.connect(imageTableModel.setLastPipelineStage)

    def update(self, pipeline):
        nodeNames = pipeline.getStageNames()
        self._nodeList.clear()
        self._nodeList.addItems(nodeNames)


class TopologyEditorWidget(QWidget):
    def __init__(self, parent, jsonParser, imageTableModel):
        super().__init__(parent)

        jsonEditor = JsonEditorWidget(self, jsonParser)
        nodeList = NodeListWidget(self, imageTableModel)

        grid = QGridLayout()
        grid.addWidget(nodeList, 0, 0)
        grid.addWidget(jsonEditor, 0, 1)
        self.setLayout(grid)

        jsonParser.processingModelUpdated.connect(nodeList.update)
