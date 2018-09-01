from PyQt5.QtWidgets import QWidget, QTableView, QHeaderView, QPushButton, QGridLayout


IMAGE_SIZE = 280


class ImageGridWidget(QWidget):
    def __init__(self, parent, model):
        super().__init__(parent)
        self._imageTable = QTableView()
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
