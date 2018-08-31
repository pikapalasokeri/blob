from PyQt5.QtWidgets import QWidget, QTableView, QHeaderView
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QVariant, QAbstractTableModel
from PyQt5 import QtCore


IMAGE_SIZE = 280


class ImageTableModel(QAbstractTableModel):
    def __init__(self, parent):
        super().__init__(parent)

    def rowCount(self, parent):
        return 2

    def columnCount(self, parent):
        return 2

    def data(self, index, role):
        filePath = "/home/pikapalasokeri/blob/images/TryEdgeDetector.jpg"
        image = QImage(filePath)
        pixmap = QPixmap(image.scaledToWidth(IMAGE_SIZE))
        if role == QtCore.Qt.DecorationRole:
            print("Returning pixmap")
            print(pixmap)
            return pixmap
        if role == QtCore.Qt.SizeHintRole:
            return pixmap.size()

        return QVariant()


class ImageGridWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self._imageTable = QTableView(self)
        model = ImageTableModel(self)
        self._imageTable.setModel(model)
        self._imageTable.resize(600, 800)
        self._imageTable.setShowGrid(False)
        self._imageTable.horizontalHeader().setDefaultSectionSize(IMAGE_SIZE)
        self._imageTable.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self._imageTable.horizontalHeader().setVisible(False)
        self._imageTable.verticalHeader().setDefaultSectionSize(IMAGE_SIZE)
        self._imageTable.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self._imageTable.verticalHeader().setVisible(False)
