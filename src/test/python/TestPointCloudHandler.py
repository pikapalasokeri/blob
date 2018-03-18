import unittest
import PointCloudHandler

class TestPointCloudHandler(unittest.TestCase):
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
