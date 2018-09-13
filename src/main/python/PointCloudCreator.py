from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QPushButton, QListWidget, QLabel, QWidget
from PyQt5.QtGui import QPixmap


PIXMAP_SIZE = 400


class CloudCreatorWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        '''
        list of images, click one and it shows
        save button
        pixels in left image exluded
        pixels in right image included
        mouse drag for include/exclude

        +--------------------------+
        |      |      | list       |
        | img1 | img2 | ...        |
        |      |      | button     |
        +--------------------------+
        horizontal layout
          img1 = label
          img2 = label
          vertical layout
            list = listwidget
            button
        '''
        mainWidget = QWidget(self)
        mainLayout = QHBoxLayout()
        listLayout = QVBoxLayout()
        noLabel = QLabel()
        yesLabel = QLabel()

        noPixmap = QPixmap(PIXMAP_SIZE, PIXMAP_SIZE)
        yesPixmap = QPixmap(PIXMAP_SIZE, PIXMAP_SIZE)

        noLabel.setPixmap(noPixmap)
        yesLabel.setPixmap(yesPixmap)

        noLabel.resize(200, 200)
        yesLabel.resize(200, 200)

        filenameList = QListWidget()
        saveButton = QPushButton("Save")
        mainLayout.addWidget(noLabel)
        mainLayout.addWidget(yesLabel)
        listLayout.addWidget(filenameList)
        listLayout.addWidget(saveButton)
        mainLayout.addLayout(listLayout)
        mainWidget.setLayout(mainLayout)

        self.setCentralWidget(mainWidget)


class PointCloudCreator:
    def __init__(self, tableModel):
        self._tableModel = tableModel
        self._currentlySelected = []

    def launchCloudCreator(self, args):
        print("Launching cloud creator")
        print(self._currentlySelected)
        self._gui = CloudCreatorWindow()
        self._gui.show()

    def updateSelection(self, selected, deselected):
        print("Updating selection")
        for modelIndex in selected.indexes():
            self._currentlySelected.append((modelIndex.row(), modelIndex.column()))
        for modelIndex in deselected.indexes():
            self._currentlySelected.remove((modelIndex.row(), modelIndex.column()))
        self._currentlySelected.sort()
