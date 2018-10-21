import numpy as np


def rgb2grayNaive(img):
    return np.dot(img[..., :3], [1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0])


def addPointsToImage(image, points, colorIx):
    shape = image.shape
    for point in points:
        row = int(point[0])
        col = int(point[1])
        if (row < shape[0] and col < shape[1]):
            image[row, col, colorIx] = 255
