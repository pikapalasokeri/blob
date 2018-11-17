import numpy as np


def sRgbToCieXyz(rgbImage):
    a = 0.055
    gammaDenominator = 12.92
    gammaConstant = 0.04045
    gammaMask = rgbImage <= gammaConstant

    transformationMatrix = np.array([[0.4124, 0.3576, 0.1805],
                                     [0.2126, 0.7152, 0.0722],
                                     [0.0193, 0.1192, 0.9505]])

    rgbLinear = rgbImage.copy()
    rgbLinear[gammaMask] /= gammaDenominator
    rgbLinear[~gammaMask] = np.power((rgbLinear[~gammaMask] + a) / (1.0 + a), 2.4)

    numPixels = rgbImage.shape[0] * rgbImage.shape[1]
    reshaped = rgbLinear.reshape((numPixels, 3)).transpose()
    reshapedXyz = np.dot(transformationMatrix, reshaped)
    xyz = reshapedXyz.transpose().reshape(rgbImage.shape)

    return xyz


def cieXyzToSrgb(xyzImage):
    transformationMatrix = np.array([[3.2406, -1.5372, -0.4986],
                                     [-0.9689, 1.8758, 0.0415],
                                     [0.0557, -0.2040, 1.0570]])
    numPixels = xyzImage.shape[0] * xyzImage.shape[1]
    reshaped = xyzImage.reshape((numPixels, 3)).transpose()
    reshapedLinearRgb = np.dot(transformationMatrix, reshaped)
    linearRgb = reshapedLinearRgb.transpose().reshape(xyzImage.shape)
    a = 0.055
    gammaFactor = 12.92
    gammaConstant = 0.0031308
    gammaMask = linearRgb <= gammaConstant
    linearRgb[gammaMask] *= gammaFactor
    linearRgb[~gammaMask] = (1 + a) * np.power(linearRgb[~gammaMask], 1.0 / 2.4) - a

    return linearRgb


def cieXyzToCieLab(xyz):
    xyz = xyz.copy()
    xyz[..., 0] /= 0.95047
    xyz[..., 2] /= 1.089

    delta = 6.0 / 29.0
    deltaSquare = delta * delta
    deltaCube = delta * delta * delta
    mask = xyz > deltaCube

    lab = np.zeros(xyz.shape)
    lab[mask[..., 1], 0] = 116.0 * np.power(xyz[mask[..., 1], 1], 1.0 / 3.0) - 16.0
    lab[~mask[..., 1], 0] = 116.0 * (xyz[~mask[..., 1], 1] / (3.0 * deltaSquare) + 4.0 / 29.0) - 16.0

    lab[mask[..., 0], 1] += 500.0 * np.power(xyz[mask[..., 0], 0], 1.0 / 3.0)
    lab[mask[..., 1], 1] -= 500.0 * np.power(xyz[mask[..., 1], 1], 1.0 / 3.0)
    lab[~mask[..., 0], 1] += 500.0 * (xyz[~mask[..., 0], 0] / (3.0 * deltaSquare) + 4.0 / 29.0)
    lab[~mask[..., 1], 1] -= 500.0 * (xyz[~mask[..., 1], 1] / (3.0 * deltaSquare) + 4.0 / 29.0)

    lab[mask[..., 1], 2] += 200.0 * np.power(xyz[mask[..., 1], 1], 1.0 / 3.0)
    lab[mask[..., 2], 2] -= 200.0 * np.power(xyz[mask[..., 2], 2], 1.0 / 3.0)
    lab[~mask[..., 1], 2] += 200.0 * (xyz[~mask[..., 1], 1] / (3.0 * deltaSquare) + 4.0 / 29.0)
    lab[~mask[..., 2], 2] -= 200.0 * (xyz[~mask[..., 2], 2] / (3.0 * deltaSquare) + 4.0 / 29.0)

    return lab


def cieLabToCieXyz(lab):
    xyz = np.zeros(lab.shape)
    delta = 6.0 / 29.0
    deltaSquare = delta * delta

    lLayer = (lab[..., 0] + 16.0) / 116.0

    layer = lLayer + lab[..., 1] / 500.0
    mask = layer > delta
    xyz[mask, 0] = np.power(layer[mask], 3.0)
    xyz[~mask, 0] = 3.0 * deltaSquare * (layer[~mask] - 4.0 / 29.0)

    layer = lLayer
    mask = layer > delta
    xyz[mask, 1] = np.power(layer[mask], 3.0)
    xyz[~mask, 1] = 3.0 * deltaSquare * (layer[~mask] - 4.0 / 29.0)

    layer = lLayer - lab[..., 2] / 200.0
    mask = layer > delta
    xyz[mask, 2] = np.power(layer[mask], 3.0)
    xyz[~mask, 2] = 3.0 * deltaSquare * (layer[~mask] - 4.0 / 29.0)

    xyz[..., 0] *= 0.95047
    xyz[..., 2] *= 1.089

    return xyz


def rgb2grayNaive(img):
    return np.dot(img[..., :3], [1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0])


def addPointsToImage(image, points, colorIx):
    shape = image.shape
    for point in points:
        row = int(point[0])
        col = int(point[1])
        if (row < shape[0] and col < shape[1]):
            image[row, col, colorIx] = 255
