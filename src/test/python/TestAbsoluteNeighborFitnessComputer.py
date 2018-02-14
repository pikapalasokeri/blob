import unittest
import numpy as np
from TestUtilities import *
from AbsoluteNeighborFitnessComputer import AbsoluteNeighborFitnessComputer

class TestAbsoluteNeighborFitnessComputer(unittest.TestCase):
    def test_Smoke(self):
        tolerance = 1.0
        points = np.zeros((10, 2))
        c = AbsoluteNeighborFitnessComputer(points, 1.0)

