from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget
from ImageGrid import ImageGridWidget
from TopologyEditorWidget import TopologyEditorWidget, JsonParser
from ImageTableModel import ImageTableModel
import ImageGrid


class ClassifierPipelineCreator(QMainWindow):
    def __init__(self):
        super().__init__()
        self._initUi()

    def _initUi(self):
        mainWidget = QWidget(self)
        self.setCentralWidget(mainWidget)
        self.setWindowTitle("Classifier pipeline creator")

        model = ImageTableModel(self, ImageGrid.IMAGE_SIZE)
        self._jsonParser = JsonParser()
        self._jsonParser.processingModelUpdated.connect(model.setPipeline)

        imageGrid = ImageGridWidget(self, model)
        topologyEditor = TopologyEditorWidget(self, self._jsonParser)

        mainGrid = QGridLayout()
        mainGrid.addWidget(imageGrid, 0, 0)
        mainGrid.addWidget(topologyEditor, 0, 1)
        mainWidget.setLayout(mainGrid)

        self.resize(1200, 800)
        self.show()
