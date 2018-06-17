import unittest
import numpy as np
from MostPopulatedCircleFinder import MostPopulatedCircleFinder


class TestMostPopulatedCircleFinder(unittest.TestCase):
    def test_NoResult(self):
        points = np.ones((0, 2))
        f = MostPopulatedCircleFinder(points)
        result = f.get(1.0)
        self.assertEqual(result, None)

    def test_SimpleResult(self):
        points = np.ones((2, 2))
        f = MostPopulatedCircleFinder(points)
        result = f.get(1.0)
        self.assertEqual(result, (1.0, 1.0))
        result = f.get(0.0)
        self.assertEqual(result, None)
