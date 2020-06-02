#!/usr/bin/python3

import imageio
from ImageUtilities import cieXyzToSrgb, cieLabToCieXyz, sRgbToCieXyz, cieXyzToCieLab, rgb2grayNaive
import matplotlib.pyplot as plt
import numpy as np


if __name__ == "__main__":
    filePath1 = "../../images/early_tests_color/3_01.jpg"
    img1 = imageio.imread(filePath1)

    goldRgb = np.array([[[0.506, 0.365, 0.31]]])

    xyz = sRgbToCieXyz(img1 / 255.0)
    lab = cieXyzToCieLab(xyz)

    a = 0.635
    b = 0.583

    aDist = (lab[..., 1] + 128.0) / 256.0 - a
    bDist = (lab[..., 2] + 128.0) / 256.0 - b
    dist = aDist * aDist + bDist * bDist

    # super naive filtering done here for experimentation
    filtered = img1.copy()
    filtered = filtered / 255.0
    filtered[..., 0] *= np.exp(-dist * 200.0)
    filtered[..., 1] *= np.exp(-dist * 200.0)
    filtered[..., 2] *= np.exp(-dist * 200.0)

    xyz = cieLabToCieXyz(lab)
    rgb = cieXyzToSrgb(xyz)

    plt.figure()
    g = rgb2grayNaive(img1)
    plt.imshow(g, cmap="gray")

    plt.figure()
    plt.imshow(rgb2grayNaive(filtered), cmap="gray")

    plt.figure()
    plt.imshow((lab + 100.0) / 200.0)

    plt.figure()
    plt.imshow(rgb)

    plt.show()
