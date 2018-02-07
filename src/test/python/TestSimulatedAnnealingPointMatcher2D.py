import unittest
import numpy as np
from SimulatedAnnealingPointMatcher2D import *
from MeanShortestDistanceFitnessComputer import *
from TestUtilities import *

class TestSimulatedAnnealingPointMatcher(unittest.TestCase):
    def test_SetFunctionsSmoke(self):
        c = MeanShortestDistanceFitnessComputer(np.zeros((0, 2)))
        m = SimulatedAnnealingPointMatcher2D(c)
        m.setNumIterations(10)
        m.setStartTemperature(1.0)
        m.setInitialRotationSigma(2.0)
        m.setSlowRotationSigma(1.0)
        m.setInitialTranslationSigma(10.0)
        m.setSlowTranslationSigma(2.0)
        m.setSlowMovementBreakpoint(0.50)
        m.setVerbose(True)
        m.setNumThreads(2)

    def test_SimpleMatch(self):
        points, dummy = getSimplePatterns()

        pointsAsNpArray = np.array(points)
        R = getRotationMatrix(35+180)
        translation = np.array([[0.11, -0.03]])
        points2 = transform(1.0, R, translation, pointsAsNpArray)

        c = MeanShortestDistanceFitnessComputer(points2)
        m = SimulatedAnnealingPointMatcher2D(c)

        addPointsToMatcher(points, m, 1)
        m.setSlowMovementBreakpoint(0.75)
        m.setInitialTranslationSigma(0.2)
        m.setSlowTranslationSigma(0.01)
        m.setStartTemperature(0.05)
        m.setNumIterations(200)

        scale, rotation, translation = m.match()

        self.assertAlmostEquals(scale, 1.0)
        numDigits = 2
        self.assertMatrixAlmostEquals(rotation, R, numDigits)
        self.assertMatrixAlmostEquals(translation, translation, numDigits)


    def assertMatrixAlmostEquals(self, matrix1, matrix2, numDigits = 7):
        self.assertEquals(matrix1.shape, matrix2.shape)

        for row1, row2 in zip(matrix1, matrix2):
            for val1, val2 in zip(row1, row2):
                self.assertAlmostEqual(val1, val2, numDigits)
