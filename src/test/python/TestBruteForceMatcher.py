import unittest
from BruteForceMatcher import BruteForceMatcher
from MeanShortestDistanceFitnessComputer import MeanShortestDistanceFitnessComputer
from AbsoluteNeighborFitnessComputer import AbsoluteNeighborFitnessComputer
import TestUtilities as Utils
import numpy as np


class TestBruteForceMatcher(unittest.TestCase):
    def test_SetFunctionsSmoke(self):
        refCloud = np.zeros((0, 2))
        c = AbsoluteNeighborFitnessComputer(refCloud, 1.0)
        m = BruteForceMatcher(c, refCloud)
        m.setCandidateKeepRatio(1)

    def test_SimpleMatch(self):
        refCloud = np.array([[0.0, 0.0],
                             [0.0, 1.0],
                             [1.0, 1.0]])
        scale = 1.0
        rotation = Utils.getRotationMatrix(90)
        translation = np.array([[1.0, 2.0]])
        matchCloud = Utils.transform(scale, rotation, translation, refCloud)

        c = MeanShortestDistanceFitnessComputer(refCloud)
        m = BruteForceMatcher(c, refCloud)
        m.setCandidateKeepRatio(1)
        scale, rotation, translation, fitness = m.match(matchCloud)

        self.assertAlmostEqual(fitness[0, 0], 0.0)
        self.assertEqual(scale[0, 0], 1.0)
        self.assertAlmostEqual(rotation[0, 0], 0.0)
        self.assertAlmostEqual(rotation[0, 1], 1.0)
        self.assertAlmostEqual(rotation[1, 0], -1.0)
        self.assertAlmostEqual(rotation[1, 1], 0.0)
