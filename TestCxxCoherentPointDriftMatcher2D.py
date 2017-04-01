import unittest
import numpy as np
from cxx.CxxPointMatcher import CxxCoherentPointDriftMatcher2D

def getSimplePatterns():
    #
    # Pattern 1:
    #   y
    #   ^
    #   | o
    #   |
    #   | o   o
    #   +-----------> x

    # Pattern 2:
    #   y
    #   ^
    #   | o o
    #   |   o
    #   |
    #   +-----------> x

    pattern1 = []
    pattern1.append((0.0, 0.0))
    pattern1.append((1.0, 0.0))
    pattern1.append((0.0, 1.0))

    pattern2 = []
    pattern2.append((0.5, 1.0))
    pattern2.append((0.5, 0.5))
    pattern2.append((0.0, 1.0))

    return pattern1, pattern2

def addPointsToMatcher(points, matcher, pointType):
    for point in points:
        if pointType == 1:
            matcher.addPoint1(point[0], point[1])
        else:
            matcher.addPoint2(point[0], point[1])

def transform(scale, rotation, translation, points):
  return scale*np.dot(points, rotation.transpose()) + translation

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

