from PointCloud import PointCloud
import json


def getPointCloudFromIterable(readable):
    return json.load(readable, cls=PointCloudJsonDecoder)


def savePointCloudToWriteable(pointCloud, writeable):
    json.dump(pointCloud, writeable, cls=PointCloudJsonEncoder, indent=2, sort_keys=True)


class PointCloudJsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, PointCloud):
            points = []
            for point in obj:
                points.append({"x": point[0],
                               "y": point[1]})

            return {
                "__type__": "PointCloud",
                "points": points,
            }
        else:
            return json.JSONEncoder.default(self, obj)


class PointCloudJsonDecoder(json.JSONDecoder):
    def __init__(self, *args, **kargs):
        json.JSONDecoder.__init__(self, object_hook=self.dict_to_object)

    def dict_to_object(self, d):
        if "__type__" not in d:
            return d

        if d["__type__"] == "PointCloud":
            result = PointCloud()
            for point in d["points"]:
                result.addXY(point["x"], point["y"])
            return result

        return d
