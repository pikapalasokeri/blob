from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QVariant, QAbstractTableModel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5 import QtCore


COLUMN_COUNT = 2


class Executor:
    def execute(self, image):
        return image


class ImageTableModel(QAbstractTableModel):
    def __init__(self, parent, imageSize):
        super().__init__(parent)
        self._rowCount = 0
        self._imageSize = imageSize
        self._pipeline = None
        self._currentLastStage = None
        self._originalImages = []
        self._currentPixmaps = []

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

    def setLastPipelineState(self, lastStage):
        self._currentLastStage = lastStage
        self._executePipelineUntil(self._currentLastStage)

    def loadNewImages(self, arg):
        filePaths = QFileDialog.getOpenFileNames(caption="Select one or more images to open",
                                                 filter="Images (*.jpg *.png)")[0]
        if len(filePaths) > 0:
            self.beginResetModel()

            self._originalFiles = filePaths
            self._originalImages = [QImage(path) for path in filePaths]
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
                processedImage = self._pipeline.executeUntil(stageName, image)
                self._currentPixmaps.append(QPixmap(processedImage.scaledToWidth(self._imageSize)))

        self.endResetModel()
