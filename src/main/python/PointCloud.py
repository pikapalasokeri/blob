import numpy as np


class PointCloud:
    def __init__(self):
        self._points = np.empty([0, 2])

    def addXY(self, x, y):
        self._points = np.append(self._points, [[x, y]], axis=0)

    def addPoint(self, point):
        self._points = np.append(self._points, [point], axis=0)

    def size(self):
        return self._points.shape[0]

    def __iter__(self):
        for point in self._points:
            yield point
