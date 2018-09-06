import unittest
from scipy import misc
import numpy as np
import os
from EdgeDetector import EdgeDetector
from ImageUtilities import rgb2grayNaive
from PointCloud import PointCloud


def readImage(relativePath):
    # Ugly hack since python unittests depend on files.
    # Copy test files somewhere before running test instead.
    dirName = os.path.dirname(__file__)
    path = os.path.join(dirName, relativePath)
    return misc.imread(path)


class TestEdgeDetector(unittest.TestCase):
    def test_SimpleCreate(self):
        randomImage = np.random.rand(2, 2)
        EdgeDetector(randomImage)

    def test_WrongImageDimensions(self):
        wrongDimensions1 = np.random.rand(1, 1, 1)
        wrongDimensions2 = np.random.rand(1)
        with self.assertRaises(Exception):
            EdgeDetector(wrongDimensions1)
        with self.assertRaises(Exception):
            EdgeDetector(wrongDimensions2)

    def test_SimpleImage(self):
        simpleImage = np.zeros((12, 12))
        simpleImage[1, 1] = 255

        expectedPointCloud = PointCloud()
        expectedPointCloud.addXY(0.5, 0.0)
        expectedPointCloud.addXY(1.5, 2.0)
        expectedPointCloud.addXY(0.0, 0.5)
        expectedPointCloud.addXY(2.0, 1.5)

        e = EdgeDetector(simpleImage)
        pointCloud = e.getEdges(1.0, 17.0)

        for point, expectedPoint in zip(pointCloud, expectedPointCloud):
            self.assertEqual(point[0], expectedPoint[0])
            self.assertEqual(point[1], expectedPoint[1])

    def test_RealImage(self):
        image = rgb2grayNaive(readImage("images_unittest/1.jpg"))
        e = EdgeDetector(image)
        cloud = e.getEdges(2.2, 6.5)
        self.assertEqual(cloud.size(), 300)

        fewPointsCloud = e.getEdges(2.2, 26.0)
        self.assertEqual(fewPointsCloud.size(), 2)

        noPointsCloud = e.getEdges(2.2, 27.0)
        self.assertEqual(noPointsCloud.size(), 0)

    def test_EmptyImage(self):
        emptyImage = np.zeros((0, 0))
        e = EdgeDetector(emptyImage)
        noPointsCloud = e.getEdges(2.0, 6.0)
        self.assertEqual(noPointsCloud.size(), 0)
