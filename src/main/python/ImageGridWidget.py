from PyQt5.QtWidgets import QWidget, QGridLayout
from PyQt5.QtGui import QPainter


class DummyWidget(QWidget):
    def __init__(self):
        super().__init__()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawRect(0, 0, 280, 280)


def addImagesToGrid(grid):
    for i in range(0, 2):
        for j in range(0, 2):
            dummyImage = DummyWidget()
            grid.addWidget(dummyImage, j, i)


class ImageGridWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        imageGrid = QGridLayout()

        addImagesToGrid(imageGrid)

        self.setLayout(imageGrid)
