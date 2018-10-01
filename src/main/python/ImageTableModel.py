from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QVariant, QAbstractTableModel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5 import QtCore
from PyQt5 import QtGui
import numpy as np


COLUMN_COUNT = 2


def qImageToMatrix(inData):
    print("+QImage to matrix")
    height = inData.height()
    width = inData.width()
    outData = np.zeros((height, width, 3))
    bytesString = inData.constBits().asstring(inData.byteCount())
    tmp = np.fromstring(bytesString, dtype=np.uint8).reshape((height, width, 4))
    outData[:, :, 2] = tmp[:, :, 0]
    outData[:, :, 1] = tmp[:, :, 1]
    outData[:, :, 0] = tmp[:, :, 2]
    print("-QImage to matrix")
    return outData


def matrixToQImage(inData):
    print("+matrix to QImage")
    height, width, channels = inData.shape
    tmp = np.ones((height, width, channels), dtype=np.uint8)
    tmp[:, :, :] = inData[:, :, :]
    outImage = QImage(tmp.data, width, height, channels * width, QtGui.QImage.Format_RGB888)
    print("-matrix to QImage")
    return outImage


class ImageTableModel(QAbstractTableModel):
    selectedImagesChanged = QtCore.pyqtSignal(list)

    def __init__(self, parent, imageSize):
        super().__init__(parent)
        self._rowCount = 0
        self._imageSize = imageSize
        self._pipeline = None
        self._currentLastStage = None
        self._originalImages = []
        self._currentPixmaps = []
        self._currentlySelected = []
        self._currentlySelectedImages = []

    def rowCount(self, parent):
        return self._rowCount

    def columnCount(self, parent):
        return COLUMN_COUNT

    def data(self, index, role):
        linearIndex = index.row() * COLUMN_COUNT + index.column()
        if linearIndex < len(self._currentPixmaps):
            pixmap = self._currentPixmaps[linearIndex]
            if role == QtCore.Qt.DecorationRole:
                return pixmap
            if role == QtCore.Qt.SizeHintRole:
                return pixmap.size()

        return QVariant()

    def setPipeline(self, pipeline):
        if self._pipeline != pipeline:
            print("set pipeline")
            self._pipeline = pipeline
            self._executePipelineUntil(self._currentLastStage)

    def setLastPipelineStage(self, lastStageItem):
        print("Setting last pipeline stage " + lastStageItem.text())
        self._currentLastStage = lastStageItem.text()
        self._executePipelineUntil(self._currentLastStage)

    def loadNewImages(self, arg):
        filePaths = QFileDialog.getOpenFileNames(caption="Select one or more images to open",
                                                 filter="Images (*.jpg *.png)")[0]
        if len(filePaths) > 0:
            self.beginResetModel()

            self._currentlySelected = []
            self._currentlySelectedImages = []
            self.selectedImagesChanged.emit(self._currentlySelectedImages)
            for path in filePaths:
                image = QImage(path)
                image.setText("path", path)
                self._originalImages.append(image)
            self._executePipelineUntil(self._currentLastStage)

            self._rowCount = int(len(self._currentPixmaps) / COLUMN_COUNT)
            if len(self._currentPixmaps) % COLUMN_COUNT > 0:
                self._rowCount += 1

            self.endResetModel()

    def _executePipelineUntil(self, stageName):
        self.beginResetModel()

        if stageName is None:
            self._currentPixmaps = [QPixmap(image.scaledToWidth(self._imageSize)) for image in self._originalImages]
        else:
            self._currentPixmaps = []
            for image in self._originalImages:
                matrixImage = qImageToMatrix(image)
                processedImage = matrixToQImage(self._pipeline.executeUntil(stageName, matrixImage))
                self._currentPixmaps.append(QPixmap(processedImage.scaledToWidth(self._imageSize)))

        self.endResetModel()

    def updateSelection(self, selected, deselected):
        print("Updating selection")
        for modelIndex in selected.indexes():
            self._currentlySelected.append((modelIndex.row(), modelIndex.column()))
        for modelIndex in deselected.indexes():
            self._currentlySelected.remove((modelIndex.row(), modelIndex.column()))
        self._currentlySelected.sort()
        print(self._currentlySelected)

        self._currentlySelectedImages = [self._originalImages[COLUMN_COUNT * i + j] for i, j in self._currentlySelected]

        self.selectedImagesChanged.emit(self._currentlySelectedImages)
        # TODO: selection must be clear whenever focus changes from imagetable,
        # or selection must be remembered and picked up again when focus changes back to imagetable
        # TODO: will out of bounds when selecting (1, 1) if only loaded 3 images for example.
