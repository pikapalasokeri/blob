import numpy as np


class PointCloud:
    def __init__(self):
        self._points = np.empty([0, 2])

    def addXY(self, x, y):
        if (type(x) != float or type(y) != float):
            raise ValueError("Point coordinates must be float")

        self._points = np.append(self._points, [[x, y]], axis=0)

    def addPoint(self, point):
        if type(point) == np.ndarray:
            if (type(point[0]) != np.float64 or type(point[1]) != np.float64):
                raise ValueError("Point coordinates must be numpy.float64 if point is numpy ndarray")
        else:
            if (type(point[0]) != float or type(point[1]) != float):
                raise ValueError("Point coordinates must be float unless point is numpy array")

        self._points = np.append(self._points, [point], axis=0)

    def size(self):
        return self._points.shape[0]

    def __iter__(self):
        for point in self._points:
            yield point
