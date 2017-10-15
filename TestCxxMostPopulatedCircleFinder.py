import unittest
import numpy as np
from cxx.CxxMostPopulatedCircleFinder import CxxMostPopulatedCircleFinder
from TestUtilities import *

class TestCxxMostPopulatedCircleFinder(unittest.TestCase):
    def test_NoResult(self):
        points = (np.zeros((0, 1)), np.zeros((0, 1)))
        f = CxxMostPopulatedCircleFinder(points)
        result = f.findCircle(1.0)
        self.assertEqual(result, None)

    def test_SimpleResult(self):
        points = (np.zeros((1, 1)), np.zeros((1, 1)))
        f = CxxMostPopulatedCircleFinder(points)
        result = f.findCircle(1.0)
        self.assertEqual(result, (0.0, 0.0))
