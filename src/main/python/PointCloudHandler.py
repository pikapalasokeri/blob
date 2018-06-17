import numpy as np
import datetime

CLOUDEXTENSION = ".cloud"
COMMENT = "#"
POINT = "p"


def getPointsFromIterable(lineIterable):
    points = []
    for l in lineIterable:
        line = l.strip()
        if len(line) == 0:
            continue
        elif line[0] == COMMENT:
            continue
        elif line[0] == POINT:
            pointLine = [_f for _f in line.split(" ") if _f]
            x = float(pointLine[1])
            y = float(pointLine[2])

            points.append((x, y))
        else:
            raise Exception("Invalid line type in CloudPoint iterable")

    numPoints = len(points)
    resultX = np.zeros((numPoints, 1))
    resultY = np.zeros((numPoints, 1))
    for i, point in enumerate(points):
        resultX[i] = point[0]
        resultY[i] = point[1]

    return resultX, resultY


def savePointCloudToWriteable(xList, yList, writeable):
    writeable.write(COMMENT + " created on " + datetime.datetime.now().isoformat() + "\n")
    for x, y in zip(xList, yList):
        writeable.write(POINT + " " + str(x[0]) + " " + str(y[0]) + "\n")
