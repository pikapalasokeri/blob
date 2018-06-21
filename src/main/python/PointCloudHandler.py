import datetime
from PointCloud import PointCloud

CLOUDEXTENSION = ".cloud"
COMMENT = "#"
POINT = "p"


def getPointCloudFromIterable(lineIterable):
    pointCloud = PointCloud()
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

            pointCloud.addXY(x, y)
        else:
            raise Exception("Invalid line type in CloudPoint iterable")

    return pointCloud


def savePointCloudToWriteable(pointCloud, writeable):
    writeable.write(COMMENT + " created on " + datetime.datetime.now().isoformat() + "\n")
    for point in pointCloud:
        writeable.write(POINT + " " + str(point[0]) + " " + str(point[1]) + "\n")
