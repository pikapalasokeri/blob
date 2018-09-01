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

    def loadNewImages(self, arg):
        filePaths = QFileDialog.getOpenFileNames(caption="Select one or more images to open",
                                                 filter="Images (*.jpg *.png)")[0]
        if len(filePaths) > 0:
            self.beginResetModel()

            self._originalFiles = filePaths
            self._originalImages = [QImage(path) for path in filePaths]
            self._currentPixmaps = [QPixmap(image.scaledToWidth(self._imageSize)) for image in self._originalImages]
            self._rowCount = int(len(self._currentPixmaps) / COLUMN_COUNT)
            if len(self._currentPixmaps) % COLUMN_COUNT > 0:
                self._rowCount += 1

            self.endResetModel()
