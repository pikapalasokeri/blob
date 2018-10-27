#!/usr/bin/python3

from PointCloudHandler import getPointCloudFromIterable
from matplotlib import pyplot as plt
import numpy as np
from PointCloud import PointCloud
from AbsoluteNeighborFitnessComputer import AbsoluteNeighborFitnessComputer
from BruteForceMatcher import BruteForceMatcher


def transform(cloud, R, T):
    newCloud = PointCloud()
    for p in cloud:
        newCloud.addPoint(np.dot(p, R.transpose()) + T)
    return newCloud


def addCloudToImage(image, cloud, colorIx):
    for point in cloud:
        row = int(point[0])
        col = int(point[1])
        image[row, col, colorIx] = 1.0


refCloudFile = "/home/pikapalasokeri/blob/resource/cloud_white_d6_basic_1.json"
cloud0File = "/home/pikapalasokeri/blob/resource/demo/1_with_edges_0.json"
cloud1File = "/home/pikapalasokeri/blob/resource/demo/1_with_edges_1.json"

with open(refCloudFile) as f:
    refCloud = getPointCloudFromIterable(f)
with open(cloud0File) as f:
    cloud0 = getPointCloudFromIterable(f)
with open(cloud1File) as f:
    cloud1 = getPointCloudFromIterable(f)

tolerance = 3.0

print("Running cxx")
c = AbsoluteNeighborFitnessComputer(refCloud.asNumpyArray(), tolerance)
cxxBruteForce = BruteForceMatcher(c, refCloud.asNumpyArray())
cxxBruteForce.setCandidateKeepRatio(1)
cxxBruteForce.setCandidateDistanceTolerance(0.05)
scale, rotation, translation, fitness = cxxBruteForce.match(cloud0.asNumpyArray())
print(scale)
print(rotation)
print(translation)
print(fitness)
print("done")

newCloud = transform(cloud0, rotation, translation[0, :])
image = np.zeros((300, 300, 3))
addCloudToImage(image, newCloud, 2)
addCloudToImage(image, refCloud, 1)
plt.figure()
plt.imshow(image)
plt.show()
