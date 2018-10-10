import numpy as np
from PyQt5.QtGui import QImage
from PyQt5 import QtGui


def qImageToMatrix(inData):
    print("+QImage to matrix")
    height = inData.height()
    width = inData.width()
    outData = np.zeros((height, width, 3))
    bytesString = inData.constBits().asstring(inData.byteCount())
    tmp = np.fromstring(bytesString, dtype=np.uint8).reshape((height, width, 4))
    outData[:, :, 2] = tmp[:, :, 0]
    outData[:, :, 1] = tmp[:, :, 1]
    outData[:, :, 0] = tmp[:, :, 2]
    print("-QImage to matrix")
    return outData


def matrixToQImage(inData):
    print("+matrix to QImage")
    height, width, channels = inData.shape
    tmp = np.ones((height, width, channels), dtype=np.uint8)
    tmp[:, :, :] = inData[:, :, :]
    outImage = QImage(tmp.data, width, height, channels * width, QtGui.QImage.Format_RGB888)
    print("-matrix to QImage")
    return outImage
