import unittest
from PointCloud import PointCloud


class TestPointCloud(unittest.TestCase):
    def test_Empty(self):
        c = PointCloud()
        self.assertEquals(c.size(), 0)

    def test_AddPoints(self):
        c = PointCloud()
        c.addPoint([1.0, 2.0])
        c.addXY(3.0, 4.0)

        points = [p for p in c]
        self.assertEquals(points[0][0], 1.0)
        self.assertEquals(points[0][1], 2.0)
        self.assertEquals(points[1][0], 3.0)
        self.assertEquals(points[1][1], 4.0)
