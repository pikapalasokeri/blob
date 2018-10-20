import unittest
import numpy as np
from SimulatedAnnealingPointMatcher2D import SimulatedAnnealingPointMatcher2D
from MeanShortestDistanceFitnessComputer import MeanShortestDistanceFitnessComputer
from AbsoluteNeighborFitnessComputer import AbsoluteNeighborFitnessComputer
import TestUtilities as Utils


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

    def test_SimpleMatchMeanShortestDistance(self):
        points, dummy = Utils.getSimplePatterns()

        pointsAsNpArray = np.array(points)
        R = Utils.getRotationMatrix(35 + 180)
        translation = np.array([[0.11, -0.03]])
        points2 = Utils.transform(1.0, R, translation, pointsAsNpArray)

        c = MeanShortestDistanceFitnessComputer(points2)
        m = SimulatedAnnealingPointMatcher2D(c)

        Utils.addPointsToAnnealer(points, m)
        m.setSlowMovementBreakpoint(0.75)
        m.setInitialTranslationSigma(0.2)
        m.setSlowTranslationSigma(0.01)
        m.setStartTemperature(0.05)
        m.setNumIterations(200)

        scale, rotation, translation, fitness = m.match()

        self.assertAlmostEqual(fitness[0, 0], 0.0, places=4)
        self.assertAlmostEqual(scale[0, 0], 1.0)
        numDigits = 2
        self.assertMatrixAlmostEquals(rotation, R, numDigits)
        self.assertMatrixAlmostEquals(translation, translation, numDigits)

    def test_SimpleMatchAbsoluteNeighbor(self):
        points, dummy = Utils.getSimplePatterns()

        pointsAsNpArray = np.array(points)
        R = Utils.getRotationMatrix(35 + 180)
        translation = np.array([[0.11, -0.03]])
        points2 = Utils.transform(1.0, R, translation, pointsAsNpArray)

        c = AbsoluteNeighborFitnessComputer(points2, 0.1)
        m = SimulatedAnnealingPointMatcher2D(c)

        Utils.addPointsToAnnealer(points, m)
        m.setSlowMovementBreakpoint(0.75)
        m.setInitialRotationSigma(360)
        m.setInitialTranslationSigma(0.2)
        m.setSlowTranslationSigma(0.1)
        m.setStartTemperature(0.0)
        m.setNumIterations(200)

        scale, rotation, translation, fitness = m.match()

        self.assertAlmostEqual(fitness[0, 0], 0.0)
        self.assertAlmostEqual(scale[0, 0], 1.0)
        numDigits = 1
        self.assertMatrixAlmostEquals(rotation, R, numDigits)
        self.assertMatrixAlmostEquals(translation, translation, numDigits)

    def assertMatrixAlmostEquals(self, matrix1, matrix2, numDigits=7):
        self.assertEqual(matrix1.shape, matrix2.shape)

        for row1, row2 in zip(matrix1, matrix2):
            for val1, val2 in zip(row1, row2):
                self.assertAlmostEqual(val1, val2, numDigits)
