from PyQt5.QtWidgets import QWidget, QGridLayout, QPlainTextEdit, QListWidget
from PyQt5.QtCore import pyqtSignal


class JsonTextEdit(QPlainTextEdit):
    newTextChanged = pyqtSignal(str)

    def __init__(self, text, parent):
        super().__init__(text, parent)
        self.textChanged.connect(self.newTextChangedProxy)

    def newTextChangedProxy(self):
        self.newTextChanged.emit(self.toPlainText())


class JsonEditorWidget(QWidget):
    def __init__(self, parent, jsonKeeper):
        super().__init__(parent)
        editor = JsonTextEdit('[\n'
                              '{\n'
                              '"name": "crop",\n'
                              '"type": "Crop",\n'
                              '"x": 0.5,\n'
                              '"y": 0.5,\n'
                              '"width": 0.5,\n'
                              '"height": 0.5\n'
                              '},\n'
                              '{\n'
                              '"name": "gray",\n'
                              '"type": "GrayscaleConversion"\n'
                              '},\n'
                              '{\n'
                              '"name": "edges",\n'
                              '"type": "EdgeDetector",\n'
                              '"sigma": 5.0,\n'
                              '"threshold": 1.0\n'
                              '},\n'
                              '{\n'
                              '"name": "keepinside",\n'
                              '"type": "KeepInsideRadius",\n'
                              '"radius": 50.0\n'
                              '},\n'
                              '{\n'
                              '"name": "annealing",\n'
                              '"type": "SimulatedAnnealing",\n'
                              '"reference_pointclouds": [{"filepath": "/home/pikapalasokeri/clouds/test1.json",\n'
                              '                  "name": "test1"},\n'
                              '                 {"filepath": "/home/pikapalasokeri/clouds/test2.json",\n'
                              '                  "name": "test2"}],\n'
                              '"annealer_settings": {}\n'
                              '},\n'
                              '{\n'
                              '"name": "stage2",\n'
                              '"type": "Nop"\n'
                              '}\n'
                              ']', self)
        editor.setStyleSheet("QPlainTextEdit{font-family: Courier New;}")
        editor.resize(400, 700)

        editor.newTextChanged.connect(jsonKeeper.tryUpdate)


class NodeListWidget(QWidget):
    def __init__(self, parent, imageTableModel, pointCloudCreator):
        super().__init__(parent)
        self._nodeList = QListWidget(self)
        self._nodeList.resize(200, 400)
        self._nodeList.itemClicked.connect(imageTableModel.setLastPipelineStage)
        self._nodeList.itemClicked.connect(pointCloudCreator.setLastPipelineStage)

    def update(self, pipeline):
        nodeNames = pipeline.getStageNames()
        self._nodeList.clear()
        self._nodeList.addItems(nodeNames)


class TopologyEditorWidget(QWidget):
    def __init__(self, parent, jsonKeeper, imageTableModel, pointCloudCreator):
        super().__init__(parent)

        jsonEditor = JsonEditorWidget(self, jsonKeeper)
        nodeList = NodeListWidget(self, imageTableModel, pointCloudCreator)

        grid = QGridLayout()
        grid.addWidget(nodeList, 0, 0)
        grid.addWidget(jsonEditor, 0, 1)
        self.setLayout(grid)

        jsonKeeper.processingModelUpdated.connect(nodeList.update)
