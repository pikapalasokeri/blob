from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QPushButton, QListWidget, QLabel, QWidget
from PyQt5.QtGui import QPixmap, QColor, QPainter
from PyQt5.QtCore import pyqtSignal
import os


PIXMAP_SIZE = 400


class SelectableQLabel(QLabel):
    rectangleSelected = pyqtSignal(tuple)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._mousePressed = False
        self._pressCoordinates = None

    def setBackgroundPixmap(self, pixmap):
        self._originalPixmap = pixmap.copy()
        self.setPixmap(pixmap)

    def mousePressEvent(self, event):
        self._mousePressed = True
        self._pressCoordinates = (event.x(), event.y())

    def mouseReleaseEvent(self, event):
        self._mousePressed = False
        self._resetDisplayPixmap()
        self.rectangleSelected.emit((self._pressCoordinates[0],
                                     self._pressCoordinates[1],
                                     event.x(),
                                     event.y()))

    def mouseMoveEvent(self, event):
        if self._mousePressed:
            self._draw(event)

    def _draw(self, event):
        newPixmap = self._originalPixmap.copy()
        painter = QPainter(newPixmap)
        painter.setBrush(QColor(255, 255, 255, 50))
        painter.setPen(QColor(255, 255, 255, 255))

        x = self._pressCoordinates[0]
        y = self._pressCoordinates[1]
        w = event.x() - x
        h = event.y() - y
        painter.drawRect(x, y, w, h)
        painter.end()

        self.setPixmap(newPixmap)

        self.repaint()

    def _resetDisplayPixmap(self):
        self.setPixmap(self._originalPixmap)


class CloudCreatorWindow(QMainWindow):
    def __init__(self, tracker, parent=None):
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
        noLabel = SelectableQLabel()
        yesLabel = SelectableQLabel()
        noLabel.rectangleSelected.connect(tracker.noRectangle)
        yesLabel.rectangleSelected.connect(tracker.yesRectangle)

        noPixmap = QPixmap(PIXMAP_SIZE, PIXMAP_SIZE)
        yesPixmap = QPixmap(PIXMAP_SIZE, PIXMAP_SIZE)

        noLabel.setBackgroundPixmap(noPixmap)
        yesLabel.setBackgroundPixmap(yesPixmap)

        noLabel.resize(200, 200)
        yesLabel.resize(200, 200)

        self._filenameList = QListWidget()
        self._filenameList.itemClicked.connect(tracker.filenameClicked)
        self.setListItems(tracker.getFilenames())
        saveButton = QPushButton("Save")
        mainLayout.addWidget(noLabel)
        mainLayout.addWidget(yesLabel)
        listLayout.addWidget(self._filenameList)
        listLayout.addWidget(saveButton)
        mainLayout.addLayout(listLayout)
        mainWidget.setLayout(mainLayout)

        self.setCentralWidget(mainWidget)

    def setListItems(self, items):
        self._filenameList.clear()
        self._filenameList.addItems(items)
        print("setlistitems:", items)


class CloudCreatorStateTracker:
    def __init__(self):
        self._images = []

    def filenameClicked(self, filenameItem):
        print("filenameClicked:", filenameItem.text())

    def yesRectangle(self, coordinates):
        print("Yes area selected", coordinates)

    def noRectangle(self, coordinates):
        print("No area selected", coordinates)

    def setImages(self, images):
        self._images = images
        for img in self._images:
            print(img.text("path"))

    def getFilenames(self):
        return [os.path.basename(img.text("path")) for img in self._images]


class PointCloudCreator:
    def __init__(self):
        self._cloudCreatorStateTracker = CloudCreatorStateTracker()
        self._lastPipelineStage = None
        self._pipeline = None
        self._gui = None

    def launchCloudCreator(self, args):
        print("Launching cloud creator")
        self._gui = CloudCreatorWindow(self._cloudCreatorStateTracker)
        self._gui.show()

    def setPipeline(self, pipeline):
        print("PointCloudCreator.setPipeline")
        self._pipeline = pipeline

    def setLastPipelineStage(self, lastStageItem):
        print("PointCloudCreator.setLastPipelineStage:", lastStageItem.text())
        self._lastPipelineStage = lastStageItem.text()

    def updateSelectedImages(self, newSelection):
        print("PointCloudCreator updateSelectedImages")
        self._cloudCreatorStateTracker.setImages(newSelection)
        if self._gui is not None:
            self._gui.setListItems(self._cloudCreatorStateTracker.getFilenames())
