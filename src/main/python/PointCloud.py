import numpy as np


class PointCloud:
    def __init__(self):
        self._points = np.empty([0, 2])
        self._max = (None, None)
        self._min = (None, None)

    def addXY(self, x, y):
        if (type(x) != float or type(y) != float):
            raise ValueError("Point coordinates must be float")

        self._points = np.append(self._points, [[x, y]], axis=0)
        self._updateMaxMin([x, y])

    def addPoint(self, point):
        if type(point) == np.ndarray:
            if (type(point[0]) != np.float64 or type(point[1]) != np.float64):
                raise ValueError("Point coordinates must be numpy.float64 if point is numpy ndarray")
        else:
            if (type(point[0]) != float or type(point[1]) != float):
                raise ValueError("Point coordinates must be float unless point is numpy array")

        self._points = np.append(self._points, [point], axis=0)
        self._updateMaxMin(point)

    def size(self):
        return self._points.shape[0]

    def min(self):
        return self._min

    def max(self):
        return self._max

    def __iter__(self):
        for point in self._points:
            yield point

    def _updateMaxMin(self, point):
        if self._max[0] is not None:
            self._max = (max(self._max[0], point[0]),
                         max(self._max[1], point[1]))
            self._min = (min(self._min[0], point[0]),
                         min(self._min[1], point[1]))
        else:
            self._max = (point[0], point[1])
            self._min = (point[0], point[1])
