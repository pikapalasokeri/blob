import unittest
import PointCloudHandler
from PointCloud import PointCloud
from PointCloudHandler import PointCloudJsonEncoder
from PointCloudHandler import PointCloudJsonDecoder


# Might be a bit overkill to test the json encoder and decoder here, but why not?
class TestJsonEncoder(unittest.TestCase):
    def test_empty(self):
        encoder = PointCloudJsonEncoder()
        cloud = PointCloud()
        jsonDict = encoder.default(cloud)
        self.assertEqual(jsonDict, {'__type__': 'PointCloud',
                                    'points': []})

    def test_simple(self):
        encoder = PointCloudJsonEncoder()
        cloud = PointCloud()
        cloud.addXY(0.0, 1.0)
        cloud.addXY(2.0, 3.0)
        jsonDict = encoder.default(cloud)
        self.assertEqual(jsonDict, {'__type__': 'PointCloud',
                                    'points': [{'x': 0.0, 'y': 1.0}, {'x': 2.0, 'y': 3.0}]})


class TestJsonDecoder(unittest.TestCase):
    def test_empty(self):
        decoder = PointCloudJsonDecoder()
        d = {"__type__": "PointCloud", "points": []}
        cloud = decoder.dict_to_object(d)
        self.assertEqual(type(cloud), PointCloud)
        self.assertEqual(cloud.size(), 0)

    def test_mustHavePointList(self):
        decoder = PointCloudJsonDecoder()
        d = {"__type__": "PointCloud"}
        with self.assertRaises(KeyError):
            decoder.dict_to_object(d)

    def test_notPointCloud(self):
        decoder = PointCloudJsonDecoder()
        d = {"points": []}
        notCloud = decoder.dict_to_object(d)
        self.assertEquals(type(notCloud), dict)

    def test_simple(self):
        decoder = PointCloudJsonDecoder()
        d = {"__type__": "PointCloud",
             "points": [{"x": 0.0, "y": 1.0},
                        {"x": 2.0, "y": 3.0}]}
        cloud = decoder.dict_to_object(d)
        self.assertEqual(type(cloud), PointCloud)
        self.assertEqual(cloud.size(), 2)
        value = 0.0
        for point in cloud:
            self.assertEqual(point[0], value)
            value += 1.0
            self.assertEqual(point[1], value)
            value += 1.0


class TestSavePointCloudToWriteable(unittest.TestCase):
    class StringStorer:
        def __init__(self):
            self.strings = []

        def write(self, string):
            self.strings.append(string)

    def test_SimpleWrite(self):
        cloud = PointCloud()
        cloud.addXY(0.0, 0.0)
        cloud.addXY(1.0, 2.0)

        writeable = self.StringStorer()
        PointCloudHandler.savePointCloudToWriteable(cloud, writeable)

        oneString = "".join(writeable.strings)
        expectedString = '{\n'\
                         '  "__type__": "PointCloud",\n'\
                         '  "points": [\n'\
                         '    {\n'\
                         '      "x": 0.0,\n'\
                         '      "y": 0.0\n'\
                         '    },\n'\
                         '    {\n'\
                         '      "x": 1.0,\n'\
                         '      "y": 2.0\n'\
                         '    }\n'\
                         '  ]\n'\
                         '}'
        self.assertEquals(oneString, expectedString)


class TestGetPointsFromIterable(unittest.TestCase):
    class Readable:
        def __init__(self, string):
            self.string = string
            self.pointer = 0

        def read(self, size=None):
            if size is None or size < 0:
                return self.string

            if self.pointer >= len(self.string):
                return ""

            result = self.string[self.pointer:min(self.pointer + size, len(self.string))]
            self.pointer += size
            return result

    def test_SinglePoint(self):
        lines = '{\n'\
                '  "__type__": "PointCloud",\n'\
                '  "points": [\n'\
                '    {\n'\
                '      "x": 1.32,\n'\
                '      "y": -1.0\n'\
                '    }\n'\
                '  ]\n'\
                '}'
        stringReader = self.Readable(lines)

        cloud = PointCloudHandler.getPointCloudFromIterable(stringReader)
        points = [p for p in cloud]

        self.assertEqual(cloud.size(), 1)
        self.assertAlmostEqual(points[0][0], 1.32)
        self.assertAlmostEqual(points[0][1], -1.0)

    def test_InvalidType(self):
        readable = self.Readable('{"someRandomStuff": "random string"}')
        self.assertNotEqual(type(PointCloudHandler.getPointCloudFromIterable(readable)), PointCloud)

    def test_MultiLine(self):
        string = '{\n'\
                 '  "__type__": "PointCloud",\n'\
                 '  "points": [\n'\
                 '    {\n'\
                 '      "x": 1.0,\n'\
                 '      "y": 0.1\n'\
                 '    },\n'\
                 '    {\n'\
                 '      "x": 2.0,\n'\
                 '      "y": -2.0\n'\
                 '    }\n'\
                 '  ]\n'\
                 '}'
        readable = self.Readable(string)
        cloud = PointCloudHandler.getPointCloudFromIterable(readable)
        points = [p for p in cloud]

        self.assertEqual(cloud.size(), 2)
        self.assertAlmostEqual(points[0][0], 1.0)
        self.assertAlmostEqual(points[0][1], 0.1)
        self.assertAlmostEqual(points[1][0], 2.0)
        self.assertAlmostEqual(points[1][1], -2.0)

    def test_NotAFloat(self):
        lines = '{\n'\
                '  "__type__": "PointCloud",\n'\
                '  "points": [\n'\
                '    {\n'\
                '      "x": "string not a float",\n'\
                '      "y": -1.0\n'\
                '    }\n'\
                '  ]\n'\
                '}'
        readable = self.Readable(lines)

        with self.assertRaises(ValueError):
            PointCloudHandler.getPointCloudFromIterable(readable)
