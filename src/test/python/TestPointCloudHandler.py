import unittest
import PointCloudHandler
from PointCloud import PointCloud


class TestSavePointCloudToWriteable(unittest.TestCase):
    class StringStorer:
        def __init__(self):
            self.strings = []

        def write(self, string):
            self.strings.append(string)

    def test_SimpleWrite(self):
        cloud = PointCloud()
        cloud.addXY(0.0, 0.0)
        cloud.addXY(1.0, 2.0)

        writeable = self.StringStorer()
        PointCloudHandler.savePointCloudToWriteable(cloud, writeable)

        self.assertEqual(len(writeable.strings), 3)
        self.assertEqual(len(writeable.strings[0]), 12 + 28)
        self.assertEqual(writeable.strings[0][0:12], "# created on")
        self.assertEqual(writeable.strings[1], "p 0.0 0.0\n")
        self.assertEqual(writeable.strings[2], "p 1.0 2.0\n")


class TestGetPointsFromIterable(unittest.TestCase):
    def test_SinglePoint(self):
        lines = ["p 1.32 -1.0"]
        cloud = PointCloudHandler.getPointCloudFromIterable(lines)
        points = [p for p in cloud]

        self.assertEqual(cloud.size(), 1)
        self.assertAlmostEqual(points[0][0], 1.32)
        self.assertAlmostEqual(points[0][1], -1.0)

    def test_Comment(self):
        lines = ["  # p 1.0 1.0"]
        cloud = PointCloudHandler.getPointCloudFromIterable(lines)

        self.assertEqual(cloud.size(), 0)

    def test_InvalidType(self):
        lines = ["invalid"]
        with self.assertRaises(Exception):
            PointCloudHandler.getPointCloudFromIterable(lines)

    def test_MultiLine(self):
        lines = [" # comment", "", "p 1.0 0.1", "p 2.0 -2.0"]
        cloud = PointCloudHandler.getPointCloudFromIterable(lines)
        points = [p for p in cloud]

        self.assertEqual(cloud.size(), 2)
        self.assertAlmostEqual(points[0][0], 1.0)
        self.assertAlmostEqual(points[0][1], 0.1)
        self.assertAlmostEqual(points[1][0], 2.0)
        self.assertAlmostEqual(points[1][1], -2.0)

    def test_NotAFloat(self):
        lines = ["p not type"]
        with self.assertRaises(ValueError):
            PointCloudHandler.getPointCloudFromIterable(lines)
