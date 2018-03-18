import unittest
import PointCloudHandler
import numpy as np

class TestSavePointCloudToWriteable(unittest.TestCase):
    class StringStorer:
        def __init__(self):
            self.strings = []
        def write(self, string):
            self.strings.append(string)

    def test_SimpleWrite(self):
        x = np.zeros((2, 1))
        y = np.zeros((2, 1))
        x[1] = 1.0
        y[1] = 2.0

        writeable = self.StringStorer()
        PointCloudHandler.savePointCloudToWriteable(x, y, writeable)

        self.assertEqual(len(writeable.strings), 3)
        self.assertEqual(len(writeable.strings[0]), 12 + 27)
        self.assertEqual(writeable.strings[0][0:12], "# created on")
        self.assertEqual(writeable.strings[1], "p 0.0 0.0")
        self.assertEqual(writeable.strings[2], "p 1.0 2.0")

class TestGetPointsFromIterable(unittest.TestCase):
    def test_SinglePoint(self):
        lines = ["p 1.32 -1.0"]
        x, y = PointCloudHandler.getPointsFromIterable(lines)

        self.assertEqual(x.shape, (1, 1))
        self.assertEqual(y.shape, (1, 1))
        self.assertAlmostEqual(x[0], 1.32)
        self.assertAlmostEqual(y[0], -1.0)

    def test_Comment(self):
        lines = ["  # p 1.0 1.0"]
        x, y = PointCloudHandler.getPointsFromIterable(lines)

        self.assertEqual(x.shape, (0, 1))
        self.assertEqual(y.shape, (0, 1))

    def test_InvalidType(self):
        lines = ["invalid"]
        with self.assertRaises(Exception):
            PointCloudHandler.getPointsFromIterable(lines)

    def test_MultiLine(self):
        lines = [" # comment", "", "p 1.0 0.1", "p 2.0 -2.0"]
        x, y = PointCloudHandler.getPointsFromIterable(lines)

        self.assertEqual(x.shape, (2, 1))
        self.assertEqual(y.shape, (2, 1))
        self.assertAlmostEqual(x[0], 1.0)
        self.assertAlmostEqual(y[0], 0.1)
        self.assertAlmostEqual(x[1], 2.0)
        self.assertAlmostEqual(y[1], -2.0)

    def test_NotAFloat(self):
        lines = ["p not type"]
        with self.assertRaises(ValueError):
            PointCloudHandler.getPointsFromIterable(lines)
