import unittest
import numpy as np
from CoherentPointDriftMatcher2D import CoherentPointDriftMatcher2D
import TestUtilities as Utils


class TestCoherentPointDriftMatcher2D(unittest.TestCase):
    def test_SetFunctionsSmoke(self):
        m = CoherentPointDriftMatcher2D()
        m.setW(0.1)
        m.setMaxIterations(20)
        m.setMinIterations(10)
        m.setSigmaSquareChangeTolerance(0.001)

    def test_SameMatch(self):
        m = CoherentPointDriftMatcher2D()

        pattern1, _ = Utils.getSimplePatterns()
        Utils.addPointsToDrifter(pattern1, m, 1)
        Utils.addPointsToDrifter(pattern1, m, 2)

        scale, rotation, translation = m.match()
        self.assertAlmostEqual(scale[0][0], 1.0)
        self.assertMatrixAlmostEquals(rotation, np.eye(2))
        self.assertMatrixAlmostEquals(translation, np.zeros((1, 2)))

    # For some unknown reason this simple match doesn't work.
    # Either it's a bug in the c++ code, or there is some
    # weird parameter setting which has been lost.
    # The possibility that the coherent point drift matcher
    # algorithm itself is to blame is not very likely.
    @unittest.expectedFailure
    def test_SimpleMatch(self):
        m = CoherentPointDriftMatcher2D()

        p2, p1 = Utils.getSimplePatterns()
        Utils.addPointsToDrifter(p1, m, 1)
        Utils.addPointsToDrifter(p2, m, 2)

        scale, rotation, translation = m.match()
        self.assertAlmostEqual(scale, 2.0)
#        self.assertMatrixAlmostEquals(rotation, np.eye(2))
#        self.assertMatrixAlmostEquals(translation, np.zeros((1, 2)))

    def assertMatrixAlmostEquals(self, matrix1, matrix2):
        self.assertEqual(matrix1.shape, matrix2.shape)

        for row1, row2 in zip(matrix1, matrix2):
            for val1, val2 in zip(row1, row2):
                self.assertAlmostEqual(val1, val2)
