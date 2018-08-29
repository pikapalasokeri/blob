from PyQt5.QtWidgets import QWidget, QGridLayout, QPlainTextEdit, QListWidget
from PyQt5.QtCore import QObject, pyqtSignal


class Model(QObject):
    modelUpdated = pyqtSignal(int)

    def __init__(self):
        super().__init__()

    def tryUpdate(self):
        print("Trying update...")
        success = True
        if success:
            self.modelUpdated.emit(-123)


class JsonEditorWidget(QWidget):
    def __init__(self, parent, model):
        super().__init__(parent)
        editor = QPlainTextEdit(self)
        editor.setStyleSheet("QPlainTextEdit{font-family: Courier New;}")
        editor.resize(400, 700)

        editor.textChanged.connect(model.tryUpdate)


class NodeListWidget(QWidget):
    def __init__(self, parent, model):
        super().__init__(parent)
        nodeList = QListWidget(self)
        nodeList.resize(200, 400)
        self._model = model

    def update(self, nodeNames):
        print("Updating node list...")
        # read shit from model and update this list
        print(nodeNames)


def printSomething():
    print("printSomething:")


class TopologyEditorWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)

        model = Model()
        jsonEditor = JsonEditorWidget(self, model)
        nodeList = NodeListWidget(self, model)

        model.modelUpdated.connect(nodeList.update)

        grid = QGridLayout()
        grid.addWidget(nodeList, 0, 0)
        grid.addWidget(jsonEditor, 0, 1)

        self.setLayout(grid)
