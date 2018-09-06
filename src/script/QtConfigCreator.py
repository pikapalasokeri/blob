#!/usr/bin/python3

from PyQt5.QtWidgets import QApplication
import sys
from ClassifierPipelineCreator import ClassifierPipelineCreator


if __name__ == "__main__":
    app = QApplication([])
    creator = ClassifierPipelineCreator()
    sys.exit(app.exec_())
