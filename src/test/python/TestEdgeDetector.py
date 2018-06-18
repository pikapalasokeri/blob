import unittest
from scipy import misc
import numpy as np
import os
from EdgeDetector import EdgeDetector


def readImage(relativePath):
    # Ugly hack since python unittests depend on files.
    # Copy test files somewhere before running test instead.
    dirName = os.path.dirname(__file__)
    path = os.path.join(dirName, relativePath)
    return misc.imread(path)


class TestEdgeDetector(unittest.TestCase):
    def test_SimpleCreate(self):
        randomImage = np.random.rand(2, 2, 3)
        EdgeDetector(randomImage)

    def test_WrongImageDimensions(self):
        wrongDimensions1 = np.random.rand(1, 1)
        wrongDimensions2 = np.random.rand(1, 1, 1, 1)
        with self.assertRaises(Exception):
            EdgeDetector(wrongDimensions1)
        with self.assertRaises(Exception):
            EdgeDetector(wrongDimensions2)

        wrongDimensions3 = np.random.rand(1, 1, 2)
        wrongDimensions4 = np.random.rand(1, 1, 4)
        with self.assertRaises(Exception):
            EdgeDetector(wrongDimensions3)
        with self.assertRaises(Exception):
            EdgeDetector(wrongDimensions4)

    def test_SimpleImage(self):
        simpleImage = np.zeros((12, 12, 3))
        simpleImage[1, 1, 0] = 255

        e = EdgeDetector(simpleImage)
        edges = e.getEdges(1.0, 17.0, 10.0)

        self.assertEqual(edges[0][0], [0.5])
        self.assertEqual(edges[1][0], [0.0])

        self.assertEqual(edges[0][1], [1.5])
        self.assertEqual(edges[1][1], [2.0])

        self.assertEqual(edges[0][2], [0.0])
        self.assertEqual(edges[1][2], [0.5])

        self.assertEqual(edges[0][3], [2.0])
        self.assertEqual(edges[1][3], [1.5])

        points = e.getEdgesAsPoints(1.0, 17.0, 10.0)
        for ix in range(len(edges[0])):
            self.assertEqual(points[ix, 0], edges[0][ix])
            self.assertEqual(points[ix, 1], edges[1][ix])

    def test_RealImage(self):
        image = readImage("images_unittest/1.jpg")
        e = EdgeDetector(image)
        edges = e.getEdgesAsPoints(2.2, 6.5, 30)
        self.assertEqual(edges.shape, (140, 2))

        fewEdges = e.getEdgesAsPoints(2.2, 26.0, 30)
        self.assertEqual(fewEdges.shape, (2, 2))

        noEdges = e.getEdgesAsPoints(2.2, 27.0, 30)
        self.assertEqual(noEdges.shape, (0, 2))

    def test_EmptyImage(self):
        emptyImage = np.zeros((0, 0, 3))
        e = EdgeDetector(emptyImage)
        noEdges = e.getEdgesAsPoints(2.0, 6.0, 30.0)
        self.assertEqual(noEdges.shape, (0, 2))

#    def test_NoDuplicatePoints(self):
#        image = np.zeros((5, 5, 3))
#        image[2, 2, 0] = 255
#        image[2, 2, 1] = 255
#        image[2, 2, 2] = 255
#
#        e = EdgeDetector(image)
#        edges = e.getEdges(0.0, 1.0, 100.0)
#
#        for x, y in zip(edges[0], edges[1]):
#            print(x, y)
#
#        for i in range(len(edges[0])):
#            x1 = edges[0][i]
#            y1 = edges[1][i]
#            for j in range(i):
#                x2 = edges[0][j]
#                y2 = edges[1][j]
#                print("--------")
#                print(x1, y1)
#                print(x2, y2)
#                self.assertFalse((x1 == x2) and (y1 == y2))
