#!/usr/bin/python3

from PyQt5.QtWidgets import QApplication, QWidget
import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)

    mainWindow = QWidget()
    mainWindow.resize(300, 300)
    mainWindow.move(300, 300)
    mainWindow.setWindowTitle("Blob config creator")
    mainWindow.show()

    sys.exit(app.exec_())
