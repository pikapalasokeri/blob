from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget
from ImageGridWidget import ImageGridWidget


class ClassifierPipelineCreator(QMainWindow):
    def __init__(self):
        super().__init__()
        self._initUi()

    def _initUi(self):
        mainWidget = QWidget(self)
        self.setCentralWidget(mainWidget)
        self.setWindowTitle("Classifier pipeline creator")

        imageGrid = ImageGridWidget(self)

        mainGrid = QGridLayout()
        mainGrid.addWidget(imageGrid, 0, 0)
        mainWidget.setLayout(mainGrid)

        self.show()
