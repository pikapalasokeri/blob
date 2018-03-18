import unittest
from scipy import misc
import numpy as np
import sys
import os
from EdgeDetector import *

def readImage(relativePath):
    # Ugly hack since python unittests depend on files.
    # Copy test files somewhere before running test instead.
    dirName = os.path.dirname(__file__)
    path = os.path.join(dirName, relativePath)
    return misc.imread(path)

class TestEdgeDetector(unittest.TestCase):
    def test_SimpleCreate(self):
        randomImage = np.random.rand(2, 2, 3)
        tmp = EdgeDetector(randomImage)

    def test_WrongImageDimensions(self):
        wrongDimensions1 = np.random.rand(1, 1)
        wrongDimensions2 = np.random.rand(1, 1, 1, 1)
        with self.assertRaises(Exception):
            tmp = EdgeDetector(wrongDimensions1)
        with self.assertRaises(Exception):
            tmp = EdgeDetector(wrongDimensions2)

        wrongDimensions3 = np.random.rand(1, 1, 2)
        wrongDimensions4 = np.random.rand(1, 1, 4)
        with self.assertRaises(Exception):
            tmp = EdgeDetector(wrongDimensions3)
        with self.assertRaises(Exception):
            tmp = EdgeDetector(wrongDimensions4)

    def test_SimpleImage(self):
        simpleImage = np.zeros((12, 12, 3))
        simpleImage[1, 1, 0] = 255

        e = EdgeDetector(simpleImage)
        edges = e.getEdges(1.0, 17.0, 10.0)

        self.assertEqual(edges[0][0], [0.0])
        self.assertEqual(edges[1][0], [0.0])

        self.assertEqual(edges[0][1], [1.0])
        self.assertEqual(edges[1][1], [2.0])

        self.assertEqual(edges[0][2], [0.0])
        self.assertEqual(edges[1][2], [0.0])

        self.assertEqual(edges[0][3], [2.0])
        self.assertEqual(edges[1][3], [1.0])

        points = e.getEdgesAsPoints(1.0, 17.0, 10.0)
        for ix in range(len(edges[0])):
            self.assertEqual(points[ix, 0], edges[0][ix])
            self.assertEqual(points[ix, 1], edges[1][ix])

    def test_RealImage(self):
        image = readImage("images_unittest/1.jpg")
        e = EdgeDetector(image)
        edges = e.getEdgesAsPoints(2.2, 6.5, 30)
        self.assertEquals(edges.shape, (140, 2))

        fewEdges = e.getEdgesAsPoints(2.2, 26.0, 30)
        self.assertEquals(fewEdges.shape, (2, 2))

        noEdges = e.getEdgesAsPoints(2.2, 27.0, 30)
        self.assertEquals(noEdges.shape, (0, 2))

    def test_EmptyImage(self):
        emptyImage = np.zeros((0, 0, 3))
        e = EdgeDetector(emptyImage)
        noEdges = e.getEdgesAsPoints(2.0, 6.0, 30.0)
        self.assertEquals(noEdges.shape, (0, 2))