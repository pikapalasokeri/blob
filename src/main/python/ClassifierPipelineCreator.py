from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget
from ImageGrid import ImageGridWidget
from TopologyEditorWidget import TopologyEditorWidget
from ImageTableModel import ImageTableModel
from JsonPipelineParser import JsonPipelineKeeper
from PointCloudCreator import PointCloudCreator
import ImageGrid


class ClassifierPipelineCreator(QMainWindow):
    def __init__(self):
        super().__init__()
        self._initUi()

    def _initUi(self):
        mainWidget = QWidget(self)
        self.setCentralWidget(mainWidget)
        self.setWindowTitle("Classifier pipeline creator")

        self._model = ImageTableModel(self, ImageGrid.IMAGE_SIZE)
        self._jsonKeeper = JsonPipelineKeeper()
        self._jsonKeeper.processingModelUpdated.connect(self._model.setPipeline)

        self._pointCloudCreator = PointCloudCreator()
        self._jsonKeeper.processingModelUpdated.connect(self._pointCloudCreator.setPipeline)
        self._model.selectedImagesChanged.connect(self._pointCloudCreator.updateSelectedImages)
        imageGrid = ImageGridWidget(self, self._model, self._pointCloudCreator)
        topologyEditor = TopologyEditorWidget(self, self._jsonKeeper, self._model, self._pointCloudCreator)

        mainGrid = QGridLayout()
        mainGrid.addWidget(imageGrid, 0, 0)
        mainGrid.addWidget(topologyEditor, 0, 1)
        mainWidget.setLayout(mainGrid)

        self.resize(1200, 800)
        self.show()
