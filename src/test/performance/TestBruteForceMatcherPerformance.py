#!/usr/bin/python3
import unittest
from BruteForceMatcher import BruteForceMatcher
from PointCloudHandler import getPointCloudFromIterable
from AbsoluteNeighborFitnessComputer import AbsoluteNeighborFitnessComputer
import time


class TestBruteForceMatcherPerformance(unittest.TestCase):
    def test_run(self):
        cloudPaths = ["/home/pikapalasokeri/blob/resource/cloud_white_d6_basic_1.json",
                      "/home/pikapalasokeri/blob/resource/cloud_white_d6_basic_2.json",
                      "/home/pikapalasokeri/blob/resource/cloud_white_d6_basic_3.json",
                      "/home/pikapalasokeri/blob/resource/cloud_white_d6_basic_4.json",
                      "/home/pikapalasokeri/blob/resource/cloud_white_d6_basic_5.json",
                      "/home/pikapalasokeri/blob/resource/cloud_white_d6_basic_6.json"]

        clouds = []
        for jsonPath in cloudPaths:
            with open(jsonPath) as f:
                clouds.append(getPointCloudFromIterable(f))

        tolerance = 3.0
        start = time.process_time()
        for cloud1 in clouds:
            m = AbsoluteNeighborFitnessComputer(cloud1.asNumpyArray(), tolerance)
            matcher = BruteForceMatcher(m, cloud1.asNumpyArray())
            for cloud2 in clouds:
                matcher.match(cloud2.asNumpyArray())
        end = time.process_time()
        print("\nBruteForceMatcher process time: {}".format(end - start))
