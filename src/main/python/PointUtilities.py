import numpy as np


def computeSquareDistances(points1, points2):
    numPoints1 = points1.shape[0]
    numPoints2 = points2.shape[0]

    squareDistances = np.zeros((numPoints1, numPoints2))
    for i, point1 in enumerate(points1):
        for j, point2 in enumerate(points2):
            squareDistances[i, j] = computeSquareDistance(point1, point2)
    return squareDistances


def computeSquareDistance(point1, point2):
    diff = point1 - point2
    return float(diff[0]**2 + diff[1]**2)


def computeClosestNeighborLikeness(points1, points2):
    squareDistances = computeSquareDistances(points1, points2)
    from1ClosestNeighbor = np.min(squareDistances, axis=1)
    from2ClosestNeighbor = np.min(squareDistances, axis=0)
    return np.mean(from1ClosestNeighbor) + np.mean(from2ClosestNeighbor)
