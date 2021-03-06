#!/usr/bin/python3

import imageio
# from scipy import ndimage
import numpy as np
# from CoherentPointDriftMatcher2D import CoherentPointDriftMatcher2D

import matplotlib.pyplot as plt
from EdgeDetector import EdgeDetector
from timeit import default_timer as timer
from SimulatedAnnealingPointMatcher2D import SimulatedAnnealingPointMatcher2D
from MeanShortestDistanceFitnessComputer import MeanShortestDistanceFitnessComputer
from CoherentPointDriftMatcher import transform
from ImageUtilities import rgb2grayNaive
import PipelineStage
import PointUtilities


def addEdgesToImage(image, edges, colorIx):
    for row, col in zip(edges[0], edges[1]):
        image[row, col, colorIx] = 255


def addNdArrayPointsToImage(image, points, colorIx):
    for point in points:
        row = int(point[0])
        col = int(point[1])
        image[row, col, colorIx] = 255


if __name__ == "__main__":
    filePath1 = "../../images/early_tests_white/4_01.jpg"
    filePath2 = "../../images/early_tests_white/4_03.jpg"

    start = timer()
    img1 = imageio.imread(filePath1)
    img2 = imageio.imread(filePath2)
    end = timer()
    print("imread:", end - start)

    sigma = 2
    thresholdFactor = 8.0
    radius = 30

    start = timer()

    edgeDetector1 = EdgeDetector(rgb2grayNaive(img1))
    edgeDetector2 = EdgeDetector(rgb2grayNaive(img2))
    edges1 = edgeDetector1.getEdges(sigma, thresholdFactor)
    keepInsideStage = PipelineStage.KeepInsideRadiusStage(radius)
    edges1 = keepInsideStage.execute(edges1)

    edges2 = edgeDetector2.getEdges(sigma, thresholdFactor)
    keepInsideStage = PipelineStage.KeepInsideRadiusStage(radius)
    edges2 = keepInsideStage.execute(edges2)

    end = timer()
    print("edgedetector:", end - start)

    points1 = np.zeros((edges1.size(), 2))
    for ix, point in enumerate(edges1):
        points1[ix, 0] = point[0]
        points1[ix, 1] = point[1]
    print(points1.shape)
    points1 = points1[::2, :]
    print(points1.shape)

    points2 = np.zeros((edges2.size(), 2))
    for ix, point in enumerate(edges2):
        points2[ix, 0] = point[0]
        points2[ix, 1] = point[1]
    print(points2.shape)
    points2 = points2[::2, :]
    print(points2.shape)

    '''
    |
    |
    2     2
    |\ /
    | X
    |/ \
    1---1------------------
    '''
    '''
    points1 = np.zeros((2,2))
    points1[1,:] = [1.0, 0.0]

    points2 = np.zeros((2,2))
    points2[0,:] = [0, 1.0]
    points2[1,:] = [1.0, 1.0]
    '''

    # start = timer()
    # matcher = CoherentPointDriftMatcher2D(points1, points2)
    # matcher.match(0.0)
    # end = timer()
    # print "matcher.match:", end-start

    print("----------------------------------------------")
    # matcher = CxxCoherentPointDriftMatcher2D()
    # matcher.setW(0.0)
    # matcher.setMaxIterations(1)
    # matcher.setMinIterations(0)
    # matcher.setSigmaSquareChangeTolerance(0.01)

    center1 = np.mean(points1, axis=0)
    center2 = np.mean(points2, axis=0)
    points1 = points1 - center1
    points2 = points2 - center2

    fitnessComputer = MeanShortestDistanceFitnessComputer(points2)
    matcher = SimulatedAnnealingPointMatcher2D(fitnessComputer)

    for p in points1:
        matcher.addPoint(p[0], p[1])

    # matcher.setStartTemperature(10.0)
    # matcher.setInitialTranslationSigma(1.0)
    # matcher.setInitialRotationSigma(90.0)
    matcher.setNumIterations(1000)
    matcher.setVerbose(True)
    start = timer()
    scale, rotation, translation, fitness = matcher.match()

    end = timer()
    print("cxxmatcher.match:", end - start)

    # print "target", points2
    # print "before transform", points1
    transformed = transform(scale, rotation, translation, points1)
    # print "after transform", transformed

    transformed = transformed + center2
    points1 = points1 + center1
    points2 = points2 + center2

    print("Closest neighbor likeness:", PointUtilities.computeClosestNeighborLikeness(points2, transformed))

    # addEdgesToImage(img1, edges1, 0)
    # addEdgesToImage(img2, edges2, 0)

    # print points1
    addNdArrayPointsToImage(img1, points1, 0)
    addNdArrayPointsToImage(img2, points1, 0)
    addNdArrayPointsToImage(img1, points2, 0)
    addNdArrayPointsToImage(img2, points2, 0)

    # addNdArrayPointsToImage(img2, points1, 2)
    # addNdArrayPointsToImage(img1, points2, 2)
    # addNdArrayPointsToImage(img2, points2, 2)
    addNdArrayPointsToImage(img1, transformed, 1)
    addNdArrayPointsToImage(img2, transformed, 1)

    plt.figure()
    plt.imshow(img1)

    plt.figure()
    plt.imshow(img2)

    plt.show()
