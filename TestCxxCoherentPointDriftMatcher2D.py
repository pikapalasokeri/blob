import unittest
import numpy as np
from cxx.CxxPointMatcher import CxxCoherentPointDriftMatcher2D
from TestUtilities import *

class TestCxxCoherentPointDriftMatcher2D(unittest.TestCase):
    def test_SetFunctionsSmoke(self):
        m = CxxCoherentPointDriftMatcher2D()
        m.setW(0.1)
        m.setMaxIterations(20)
        m.setMinIterations(10)
        m.setSigmaSquareChangeTolerance(0.001)

    def test_SameMatch(self):
        m = CxxCoherentPointDriftMatcher2D()

        pattern1, _ = getSimplePatterns()
        addPointsToMatcher(pattern1, m, 1)
        addPointsToMatcher(pattern1, m, 2)

        scale, rotation, translation = m.match()
        self.assertAlmostEquals(scale, 1.0)
        self.assertMatrixAlmostEquals(rotation, np.eye(2))
        self.assertMatrixAlmostEquals(translation, np.zeros((1, 2)))

    # For some unknown reason this simple match doesn't work.
    # Either it's a bug in the c++ code, or there is some
    # weird parameter setting which has been lost.
    # The possibility that the coherent point drift matcher
    # algorithm itself is to blame is not very likely.
    @unittest.expectedFailure
    def test_SimpleMatch(self):
        m = CxxCoherentPointDriftMatcher2D()

        p2, p1 = getSimplePatterns()
        addPointsToMatcher(p1, m, 1)
        addPointsToMatcher(p2, m, 2)

        scale, rotation, translation = m.match()
        self.assertAlmostEquals(scale, 2.0)
#        self.assertMatrixAlmostEquals(rotation, np.eye(2))
#        self.assertMatrixAlmostEquals(translation, np.zeros((1, 2)))

    def assertMatrixAlmostEquals(self, matrix1, matrix2):
        self.assertEquals(matrix1.shape, matrix2.shape)

        for row1, row2 in zip(matrix1, matrix2):
            for val1, val2 in zip(row1, row2):
                self.assertAlmostEqual(val1, val2)

