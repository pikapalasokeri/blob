from PyQt5.QtWidgets import QWidget, QGridLayout, QPlainTextEdit, QListWidget
from PyQt5.QtCore import QObject, pyqtSignal
import json


class Model(QObject):
    modelUpdated = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self._currentNodes = []

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
                self.modelUpdated.emit(nodeNames)
        except json.JSONDecodeError as e:
            print(str(e))


class JsonTextEdit(QPlainTextEdit):
    newTextChanged = pyqtSignal(str)

    def __init__(self, parent):
        super().__init__(parent)
        self.textChanged.connect(self.newTextChangedProxy)

    def newTextChangedProxy(self):
        self.newTextChanged.emit(self.toPlainText())


class JsonEditorWidget(QWidget):
    textChangedWithText = pyqtSignal(str)

    def __init__(self, parent, model):
        super().__init__(parent)
        editor = JsonTextEdit(self)
        editor.setStyleSheet("QPlainTextEdit{font-family: Courier New;}")
        editor.resize(400, 700)

        editor.newTextChanged.connect(model.tryUpdate)


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
        self._nodeList.addItems(nodeNames)


class TopologyEditorWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        self._model = Model()
        jsonEditor = JsonEditorWidget(self, self._model)
        nodeList = NodeListWidget(self)

        self._model.modelUpdated.connect(nodeList.update)

        grid = QGridLayout()
        grid.addWidget(nodeList, 0, 0)
        grid.addWidget(jsonEditor, 0, 1)

        self.setLayout(grid)
