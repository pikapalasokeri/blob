#!/usr/bin/python3

import imageio
import matplotlib.pyplot as plt
from EdgeDetector import EdgeDetector
from ImageUtilities import rgb2grayNaive
import PipelineStage


def addEdgesToImage(image, edges, colorIx):
    for point in edges:
        row = point[0]
        col = point[1]
        image[int(row), int(col), colorIx] = 255


if __name__ == "__main__":
    filePath = "../../images/TryEdgeDetector.jpg"
    img = imageio.imread(filePath)
    edgeDetector = EdgeDetector(rgb2grayNaive(img))
    radius = 1000

    sigma = 4
    thresholdFactor = 0.4
    edges = edgeDetector.getEdges(sigma, thresholdFactor)
    keepInsideStage = PipelineStage.KeepInsideRadiusStage(radius)
    edges = keepInsideStage.execute(edges)

    print("Got", edges.size(), "edge points at sigma", sigma, "and thresholdFactor", thresholdFactor)
    addEdgesToImage(img, edges, 0)
    addEdgesToImage(img, edges, 2)

    sigma = 8
    thresholdFactor = 0.1
    edges = edgeDetector.getEdges(sigma, thresholdFactor)
    keepInsideStage = PipelineStage.KeepInsideRadiusStage(radius)
    edges = keepInsideStage.execute(edges)
    print("Got", edges.size(), "edge points at sigma", sigma, "and thresholdFactor", thresholdFactor)
    addEdgesToImage(img, edges, 1)

    sigma = 16
    thresholdFactor = 0.01
    edges = edgeDetector.getEdges(sigma, thresholdFactor)
    keepInsideStage = PipelineStage.KeepInsideRadiusStage(radius)
    edges = keepInsideStage.execute(edges)
    print("Got", edges.size(), "edge points at sigma", sigma, "and thresholdFactor", thresholdFactor)
    addEdgesToImage(img, edges, 2)

    plt.figure()
    plt.imshow(img)
    plt.show()
