import unittest
from PointCloud import PointCloud, PointCloudToRgbImage
import numpy as np


class TestPointCloud(unittest.TestCase):
    def test_Empty(self):
        c = PointCloud()
        self.assertEquals(c.size(), 0)
        self.assertEquals(c.min(), (None, None))
        self.assertEquals(c.max(), (None, None))

    def test_AddPoints(self):
        c = PointCloud()
        c.addPoint([1.0, 2.0])
        c.addXY(3.0, 4.0)

        points = [p for p in c]
        self.assertEquals(points[0][0], 1.0)
        self.assertEquals(points[0][1], 2.0)
        self.assertEquals(points[1][0], 3.0)
        self.assertEquals(points[1][1], 4.0)
        self.assertEquals(c.max(), (3.0, 4.0))
        self.assertEquals(c.min(), (1.0, 2.0))

    def test_AddNonFloatXY(self):
        c = PointCloud()
        with self.assertRaises(ValueError):
            c.addXY(2.0, "not float")

    def test_AddNonFloatPoint(self):
        c = PointCloud()
        with self.assertRaises(ValueError):
            c.addPoint(["not float", 1.0])
        # No coverage yet for ndarray float64 stuff

    def test_ToRgb(self):
        c = PointCloud()
        image = PointCloudToRgbImage(c, 0)
        rows, cols, channels = image.shape
        self.assertEquals(channels, 3)
        for element in np.nditer(image):
            self.assertEquals(element, 0.0)

        c.addXY(0.0, 0.0)
        c.addXY(10.0, 10.0)
        image = PointCloudToRgbImage(c, 0)
        rows, cols, channels = image.shape
        self.assertEquals(rows, 11)
        self.assertEquals(cols, 11)
        self.assertEquals(image[0, 0, 0], 255)
        self.assertEquals(image[0, 0, 1], 0)
        self.assertEquals(image[0, 0, 2], 0)
        self.assertEquals(image[10, 10, 0], 255)
        self.assertEquals(image[10, 10, 1], 0)
        self.assertEquals(image[10, 10, 2], 0)
        self.assertEquals(np.sum(image), 510)
