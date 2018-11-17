import unittest
import numpy as np
from ImageUtilities import sRgbToCieXyz, cieXyzToSrgb, cieXyzToCieLab, cieLabToCieXyz


r = 0.5
g = 0.04
b = 0.0

x = 0.08937768
y = 0.04771938
z = 0.00450003

ll = 26.07488329
la = 46.01295232
lb = 38.52108463


class TestRgbToXyz(unittest.TestCase):
    def test_OnePixel(self):
        image = np.array([[[r, g, b]]])
        xyz = sRgbToCieXyz(image)
        self.assertAlmostEqual(xyz[0, 0, 0], x)
        self.assertAlmostEqual(xyz[0, 0, 1], y)
        self.assertAlmostEqual(xyz[0, 0, 2], z)

    def test_TwoPixelsCols(self):
        image = np.array([[[r, g, b], [r, g, b]]])
        xyz = sRgbToCieXyz(image)
        self.assertAlmostEqual(xyz[0, 0, 0], x)
        self.assertAlmostEqual(xyz[0, 0, 1], y)
        self.assertAlmostEqual(xyz[0, 0, 2], z)
        self.assertAlmostEqual(xyz[0, 1, 0], x)
        self.assertAlmostEqual(xyz[0, 1, 1], y)
        self.assertAlmostEqual(xyz[0, 1, 2], z)

    def test_TwoPixelsRows(self):
        image = np.array([[[r, g, b]],
                          [[r, g, b]]])
        xyz = sRgbToCieXyz(image)
        self.assertAlmostEqual(xyz[0, 0, 0], x)
        self.assertAlmostEqual(xyz[0, 0, 1], y)
        self.assertAlmostEqual(xyz[0, 0, 2], z)
        self.assertAlmostEqual(xyz[1, 0, 0], x)
        self.assertAlmostEqual(xyz[1, 0, 1], y)
        self.assertAlmostEqual(xyz[1, 0, 2], z)

    def test_BlackPixel(self):
        image = np.array([[[0.0, 0.0, 0.0]]])
        xyz = sRgbToCieXyz(image)
        self.assertAlmostEqual(xyz[0, 0, 2], 0.0)

    def test_WhitePixel(self):
        image = np.array([[[1.0, 1.0, 1.0]]])
        xyz = sRgbToCieXyz(image)
        self.assertAlmostEqual(xyz[0, 0, 2], 1.089)


class TestXyzToSrgb(unittest.TestCase):
    def test_OnePixel(self):
        image = np.array([[[x, y, z]]])
        rgb = cieXyzToSrgb(image)
        self.assertAlmostEqual(rgb[0, 0, 0], r, places=5)
        self.assertAlmostEqual(rgb[0, 0, 1], g, places=3)
        self.assertAlmostEqual(rgb[0, 0, 2], b, places=5)

    def test_TwoPixelsCols(self):
        image = np.array([[[x, y, z], [x, y, z]]])
        rgb = cieXyzToSrgb(image)
        self.assertAlmostEqual(rgb[0, 0, 0], r, places=5)
        self.assertAlmostEqual(rgb[0, 0, 1], g, places=3)
        self.assertAlmostEqual(rgb[0, 0, 2], b, places=5)
        self.assertAlmostEqual(rgb[0, 1, 0], r, places=5)
        self.assertAlmostEqual(rgb[0, 1, 1], g, places=3)
        self.assertAlmostEqual(rgb[0, 1, 2], b, places=5)

    def test_TwoPixelsRows(self):
        image = np.array([[[x, y, z]],
                          [[x, y, z]]])
        rgb = cieXyzToSrgb(image)
        self.assertAlmostEqual(rgb[0, 0, 0], r, places=5)
        self.assertAlmostEqual(rgb[0, 0, 1], g, places=3)
        self.assertAlmostEqual(rgb[0, 0, 2], b, places=5)
        self.assertAlmostEqual(rgb[1, 0, 0], r, places=5)
        self.assertAlmostEqual(rgb[1, 0, 1], g, places=3)
        self.assertAlmostEqual(rgb[1, 0, 2], b, places=5)


class TestXyzToLab(unittest.TestCase):
    def test_OnePixel(self):
        image = np.array([[[x, y, z]]])
        lab = cieXyzToCieLab(image)
        self.assertAlmostEqual(lab[0, 0, 0], ll)
        self.assertAlmostEqual(lab[0, 0, 1], la)
        self.assertAlmostEqual(lab[0, 0, 2], lb)

    def test_TwoPixelsCols(self):
        image = np.array([[[x, y, z], [x, y, z]]])
        lab = cieXyzToCieLab(image)
        self.assertAlmostEqual(lab[0, 0, 0], ll)
        self.assertAlmostEqual(lab[0, 0, 1], la)
        self.assertAlmostEqual(lab[0, 0, 2], lb)
        self.assertAlmostEqual(lab[0, 1, 0], ll)
        self.assertAlmostEqual(lab[0, 1, 1], la)
        self.assertAlmostEqual(lab[0, 1, 2], lb)

    def test_TwoPixelsRows(self):
        image = np.array([[[x, y, z]],
                          [[x, y, z]]])
        lab = cieXyzToCieLab(image)
        self.assertAlmostEqual(lab[0, 0, 0], ll)
        self.assertAlmostEqual(lab[0, 0, 1], la)
        self.assertAlmostEqual(lab[0, 0, 2], lb)
        self.assertAlmostEqual(lab[1, 0, 0], ll)
        self.assertAlmostEqual(lab[1, 0, 1], la)
        self.assertAlmostEqual(lab[1, 0, 2], lb)


class TestLabToXyz(unittest.TestCase):
    def test_OnePixel(self):
        image = np.array([[[ll, la, lb]]])
        xyz = cieLabToCieXyz(image)
        self.assertAlmostEqual(xyz[0, 0, 0], x)
        self.assertAlmostEqual(xyz[0, 0, 1], y)
        self.assertAlmostEqual(xyz[0, 0, 2], z)

    def test_TwoPixelsCols(self):
        image = np.array([[[ll, la, lb], [ll, la, lb]]])
        xyz = cieLabToCieXyz(image)
        self.assertAlmostEqual(xyz[0, 0, 0], x)
        self.assertAlmostEqual(xyz[0, 0, 1], y)
        self.assertAlmostEqual(xyz[0, 0, 2], z)
        self.assertAlmostEqual(xyz[0, 1, 0], x)
        self.assertAlmostEqual(xyz[0, 1, 1], y)
        self.assertAlmostEqual(xyz[0, 1, 2], z)

    def test_TwoPixelsRows(self):
        image = np.array([[[ll, la, lb]],
                          [[ll, la, lb]]])
        xyz = cieLabToCieXyz(image)
        self.assertAlmostEqual(xyz[0, 0, 0], x)
        self.assertAlmostEqual(xyz[0, 0, 1], y)
        self.assertAlmostEqual(xyz[0, 0, 2], z)
        self.assertAlmostEqual(xyz[1, 0, 0], x)
        self.assertAlmostEqual(xyz[1, 0, 1], y)
        self.assertAlmostEqual(xyz[1, 0, 2], z)
