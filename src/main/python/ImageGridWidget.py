from PyQt5.QtWidgets import QWidget, QTableView, QHeaderView, QPushButton, QGridLayout, QFileDialog
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QVariant, QAbstractTableModel
from PyQt5 import QtCore


IMAGE_SIZE = 280
COLUMN_COUNT = 2


class ImageTableModel(QAbstractTableModel):
    def __init__(self, parent):
        super().__init__(parent)
        self._rowCount = 0

    def rowCount(self, parent):
        print("rowCount: {}".format(self._rowCount))
        return self._rowCount

    def columnCount(self, parent):
        print("columnCount: {}".format(COLUMN_COUNT))
        return COLUMN_COUNT

    def data(self, index, role):
        print("data(self, index, role)")
        linearIndex = index.row() * COLUMN_COUNT + index.column()
        if linearIndex < len(self._currentPixmaps):
            pixmap = self._currentPixmaps[linearIndex]
            if role == QtCore.Qt.DecorationRole:
                print("Returning pixmap")
                print(pixmap)
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
            self._currentPixmaps = [QPixmap(image.scaledToWidth(IMAGE_SIZE)) for image in self._originalImages]
            self._rowCount = int(len(self._currentPixmaps) / COLUMN_COUNT)
            if len(self._currentPixmaps) % COLUMN_COUNT > 0:
                self._rowCount += 1

            self.endResetModel()


class ImageGridWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self._imageTable = QTableView()
        model = ImageTableModel(self)
        self._imageTable.setModel(model)
        self._imageTable.setShowGrid(False)
        self._imageTable.horizontalHeader().setDefaultSectionSize(IMAGE_SIZE)
        self._imageTable.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self._imageTable.horizontalHeader().setVisible(False)
        self._imageTable.verticalHeader().setDefaultSectionSize(IMAGE_SIZE)
        self._imageTable.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self._imageTable.verticalHeader().setVisible(False)

        loadButton = QPushButton("Open")
        loadButton.clicked.connect(model.loadNewImages)

        layout = QGridLayout()
        layout.addWidget(self._imageTable, 0, 0)
        layout.addWidget(loadButton, 1, 0)
        self.setLayout(layout)
        self.setMaximumWidth(600)
