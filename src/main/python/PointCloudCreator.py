from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QVBoxLayout, QPushButton, QListWidget, QLabel, QWidget
from PyQt5.QtGui import QPixmap, QColor, QPainter
from PyQt5.QtCore import QObject, pyqtSignal
import os
from PointCloud import PointCloud
from QImageUtilities import qImageToMatrix


PIXMAP_SIZE = 400


def exchangePoints(fromCloud, toCloud, coordinates):
    xBox = sorted([coordinates[1], coordinates[3]])
    yBox = sorted([coordinates[0], coordinates[2]])
    retFromCloud = PointCloud()

    # TODO: Break out duplicated code.
    xMin, yMin = fromCloud.min()
    xMax, yMax = fromCloud.max()
    xCenter = (xMin + xMax) / 2
    yCenter = (yMin + yMax) / 2
    width = xMax - xMin
    height = yMax - yMin
    size = max(width, height)

    for point in fromCloud:
        x = (point[0] - xCenter) / size * PIXMAP_SIZE + PIXMAP_SIZE / 2
        y = (point[1] - yCenter) / size * PIXMAP_SIZE + PIXMAP_SIZE / 2

        if(x >= xBox[0] and
           x <= xBox[1] and
           y >= yBox[0] and
           y <= yBox[1]):
            toCloud.addPoint(point)
        else:
            retFromCloud.addPoint(point)
    return retFromCloud, toCloud


def cloudToPixmap(pointCloud):
    pixmap = QPixmap(PIXMAP_SIZE, PIXMAP_SIZE)
    painter = QPainter(pixmap)
    painter.fillRect(0, 0, PIXMAP_SIZE, PIXMAP_SIZE, QColor(0, 0, 0, 255))

    painter.setPen(QColor(255, 0, 0, 255))

    if pointCloud.size() > 0:
        xMin, yMin = pointCloud.min()
        xMax, yMax = pointCloud.max()
        xCenter = (xMin + xMax) / 2
        yCenter = (yMin + yMax) / 2
        width = xMax - xMin
        height = yMax - yMin
        size = max(width, height)

        for point in pointCloud:
            x = (point[0] - xCenter) / size * PIXMAP_SIZE + PIXMAP_SIZE / 2
            y = (point[1] - yCenter) / size * PIXMAP_SIZE + PIXMAP_SIZE / 2
            painter.drawPoint(y, x)

    painter.end()
    return pixmap


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
        self._noLabel = SelectableQLabel()
        self._yesLabel = SelectableQLabel()
        self._noLabel.rectangleSelected.connect(tracker.noRectangle)
        self._yesLabel.rectangleSelected.connect(tracker.yesRectangle)

        noPixmap = cloudToPixmap(PointCloud())
        yesPixmap = cloudToPixmap(PointCloud())

        self._noLabel.setBackgroundPixmap(noPixmap)
        self._yesLabel.setBackgroundPixmap(yesPixmap)

        self._noLabel.resize(PIXMAP_SIZE, PIXMAP_SIZE)
        self._yesLabel.resize(PIXMAP_SIZE, PIXMAP_SIZE)

        self._filenameList = QListWidget()
        self._filenameList.itemClicked.connect(tracker.filenameClicked)
        self.setListItems(tracker.getFilenames())
        saveButton = QPushButton("Save")
        mainLayout.addWidget(self._noLabel)
        mainLayout.addWidget(self._yesLabel)
        listLayout.addWidget(self._filenameList)
        listLayout.addWidget(saveButton)
        mainLayout.addLayout(listLayout)
        mainWidget.setLayout(mainLayout)

        self.setCentralWidget(mainWidget)

    def setListItems(self, items):
        self._filenameList.clear()
        self._filenameList.addItems(items)
        print("setlistitems:", items)

    def showPointClouds(self, pointClouds):
        noCloud = pointClouds[0]
        yesCloud = pointClouds[1]
        noPixmap = cloudToPixmap(noCloud)
        yesPixmap = cloudToPixmap(yesCloud)
        self._noLabel.setBackgroundPixmap(noPixmap)
        self._yesLabel.setBackgroundPixmap(yesPixmap)


class CloudCreatorStateTracker(QObject):
    activePointCloudsChanged = pyqtSignal(tuple)

    def __init__(self):
        super().__init__()
        self._images = []
        self._filenames = []
        self._noPointClouds = {}
        self._yesPointClouds = {}
        self._activeFilename = ""
        self._activeYesPointCloud = PointCloud()
        self._activeNoPointCloud = PointCloud()
        self._pipeline = None
        self._lastPipelineStage = None

    def filenameClicked(self, filenameItem):
        filename = filenameItem.text()
        print("filenameClicked:", filename)
        self._yesPointClouds[self._activeFilename] = self._activeYesPointCloud
        self._noPointClouds[self._activeFilename] = self._activeNoPointCloud

        self._activeFilename = filename
        self._activeYesPointCloud = self._yesPointClouds[self._activeFilename]
        self._activeNoPointCloud = self._noPointClouds[self._activeFilename]
        self.activePointCloudsChanged.emit((self._activeNoPointCloud,
                                            self._activeYesPointCloud))

    def yesRectangle(self, coordinates):
        print("Yes area selected", coordinates)
        self._activeYesPointCloud, self._activeNoPointCloud = exchangePoints(self._activeYesPointCloud, self._activeNoPointCloud, coordinates)
        self.activePointCloudsChanged.emit((self._activeNoPointCloud,
                                            self._activeYesPointCloud))

    def noRectangle(self, coordinates):
        print("No area selected", coordinates)
        self._activeNoPointCloud, self._activeYesPointCloud = exchangePoints(self._activeNoPointCloud, self._activeYesPointCloud, coordinates)
        self.activePointCloudsChanged.emit((self._activeNoPointCloud,
                                            self._activeYesPointCloud))

    def setImages(self, images):
        print("setImages", len(images))
        self._images = images
        self._filenames = [os.path.basename(img.text("path")) for img in self._images]
        self._resetPointClouds()

    def getFilenames(self):
        return [os.path.basename(path) for path in self._filenames]

    def setLastPipelineStage(self, stage):
        self._lastPipelineStage = stage
        self._resetPointClouds()

    def setPipeline(self, pipeline):
        self._pipeline = pipeline
        self._resetPointClouds()

    def _resetPointClouds(self):
        print("reset point clouds")
        if (self._pipeline is not None and self._lastPipelineStage is not None):
            self._yesPointClouds = {}
            self._noPointClouds = {}
            for filename, img in zip(self._filenames, self._images):
                pointCloud = self._pipeline.executeUntilRaw(self._lastPipelineStage, qImageToMatrix(img))
                if type(pointCloud) is PointCloud:
                    print("Added point cloud with size:", pointCloud.size())
                    self._noPointClouds[filename] = pointCloud
                    self._yesPointClouds[filename] = PointCloud()
            if len(self._filenames) > 0:
                self._activeFilename = self._filenames[0]
                self._activeYesPointCloud = self._yesPointClouds[self._activeFilename]
                self._activeNoPointCloud = self._noPointClouds[self._activeFilename]
                self.activePointCloudsChanged.emit((self._activeNoPointCloud,
                                                    self._activeYesPointCloud))


class PointCloudCreator:
    def __init__(self):
        self._cloudCreatorStateTracker = CloudCreatorStateTracker()
        self._gui = None

    def launchCloudCreator(self, args):
        print("Launching cloud creator")
        self._gui = CloudCreatorWindow(self._cloudCreatorStateTracker)
        self._cloudCreatorStateTracker.activePointCloudsChanged.connect(self._gui.showPointClouds)
        self._gui.show()

    def setPipeline(self, pipeline):
        print("PointCloudCreator.setPipeline")
        self._cloudCreatorStateTracker.setPipeline(pipeline)

    def setLastPipelineStage(self, lastStageItem):
        print("PointCloudCreator.setLastPipelineStage:", lastStageItem.text())
        self._cloudCreatorStateTracker.setLastPipelineStage(lastStageItem.text())

    def updateSelectedImages(self, newSelection):
        print("PointCloudCreator updateSelectedImages")
        self._cloudCreatorStateTracker.setImages(newSelection)
        if self._gui is not None:
            self._gui.setListItems(self._cloudCreatorStateTracker.getFilenames())
