import numpy as np


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


def addPointsToDrifter(points, matcher, pointType):
    for point in points:
        if pointType == 1:
            matcher.addPoint1(point[0], point[1])
        else:
            matcher.addPoint2(point[0], point[1])


def addPointsToAnnealer(points, matcher):
    for point in points:
        matcher.addPoint(point[0], point[1])


def transform(scale, rotation, translation, points):
    return scale * np.dot(points, rotation.transpose()) + translation


def getRotationMatrix(angleDegrees):
    alphaRadians = np.pi / 180 * angleDegrees

    R = np.array([[np.cos(alphaRadians), -np.sin(alphaRadians)],
                 [np.sin(alphaRadians), np.cos(alphaRadians)]])
    return R
