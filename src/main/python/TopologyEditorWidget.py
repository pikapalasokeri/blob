from PyQt5.QtWidgets import QWidget, QGridLayout, QPlainTextEdit, QListWidget
from PyQt5.QtCore import QObject, pyqtSignal
import json


class JsonParser(QObject):
    nodesUpdated = pyqtSignal(list)

    def __init__(self):
        super().__init__()

    def tryUpdate(self, maybeJsonText):
        print("Trying update...")
        print(maybeJsonText)
        try:
            validJson = json.loads(maybeJsonText)
            if type(validJson) == list:
                nodeNames = []
                for element in validJson:
                    print("element:", element)
                    if "name" in element:
                        nodeNames.append(element["name"])
                print("validJson:")
                print(validJson)
                self.nodesUpdated.emit(nodeNames)
        except json.JSONDecodeError as e:
            print(str(e))


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
        editor = JsonTextEdit("[]", self)
        editor.setStyleSheet("QPlainTextEdit{font-family: Courier New;}")
        editor.resize(400, 700)

        editor.newTextChanged.connect(jsonParser.tryUpdate)


class NodeListWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self._nodeList = QListWidget(self)
        self._nodeList.resize(200, 400)

    def update(self, nodeNames):
        print("Updating node list...")
        # read shit from model and update this list
        print(nodeNames)
        self._nodeList.clear()
        self._nodeList.addItem(self._rawImagesNode())
        self._nodeList.addItems(nodeNames)

    def _rawImagesNode(self):
        return "Raw images"


class TopologyEditorWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self._jsonParser = JsonParser()
        jsonParser = self._jsonParser

        jsonEditor = JsonEditorWidget(self, jsonParser)
        nodeList = NodeListWidget(self)
        nodeList.update([])

        grid = QGridLayout()
        grid.addWidget(nodeList, 0, 0)
        grid.addWidget(jsonEditor, 0, 1)
        self.setLayout(grid)

        jsonParser.nodesUpdated.connect(nodeList.update)
