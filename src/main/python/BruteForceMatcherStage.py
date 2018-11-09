import numpy as np
import PointUtilities
from BruteForceMatcher import BruteForceMatcher
from AbsoluteNeighborFitnessComputer import AbsoluteNeighborFitnessComputer
from PointCloudHandler import getPointCloudFromIterable
import ImageUtilities
from PIL import Image, ImageDraw
import sys


class BruteForceMatcherStage:
    def __init__(self, pointClouds, settings):
        self._tolerance = 3.0
        self._reasonableFitnessThreshold = 0.2
        self._matchers = {}
        self._fitnessComputers = {}
        self._referenceClouds = {}
        for pointCloud in pointClouds:
            jsonPath = pointCloud["filepath"]
            referenceName = pointCloud["name"]
            print(referenceName, jsonPath)

            with open(jsonPath) as f:
                referenceCloud = getPointCloudFromIterable(f)

            center = referenceCloud.mean()
            centeredReference = np.array(referenceCloud.asNumpyArray(), copy=True)
            centeredReference[:, 0] -= center[0]
            centeredReference[:, 1] -= center[1]

            fitnessComputer = AbsoluteNeighborFitnessComputer(centeredReference, self._tolerance)
            matcher = BruteForceMatcher(fitnessComputer, centeredReference)
            for name, setting in settings.items():
                if name == "CandidateKeepRatio":
                    matcher.setCandidateKeepRatio(int(setting))
                elif name == "CandidateDistanceTolerance":
                    matcher.setCandidateDistanceTolerance(float(setting))
                else:
                    print("Unknown setting {}: {}".format(name, setting))

            # TODO: fix lifetime issues here so that we dont need to explicitly keep
            # fitnessComputer around.
            self._matchers[referenceName] = matcher
            self._fitnessComputers[referenceName] = fitnessComputer
            self._referenceClouds[referenceName] = centeredReference

    def execute(self, pointCloud):
        center = pointCloud.mean()
        centeredSample = np.array(pointCloud.asNumpyArray(), copy=True)
        centeredSample[:, 0] -= center[0]
        centeredSample[:, 1] -= center[1]
        self._lastCloud = centeredSample

        self._bestReferenceName = "none"
        matchMask = np.zeros(centeredSample.shape[0])
        reasonableReferences = []
        for referenceName, matcher in self._matchers.items():
            print("Computing for: {}".format(referenceName))
            scale, rotation, translation, fitness = matcher.match(centeredSample)
            print("Fitness: {}".format(fitness))
            if fitness < self._reasonableFitnessThreshold:
                print("Fitness is reasonable.")
                transformedSample = np.dot(centeredSample, rotation.transpose()) + translation
                matchMask = np.logical_or(matchMask, getMatchMask(transformedSample,
                                                                  self._referenceClouds[referenceName],
                                                                  self._tolerance))
                reasonableReferences.append((referenceName, scale, rotation, translation))

        bestFitness = sys.float_info.max
        for referenceName, scale, rotation, translation in reasonableReferences:
            print("Reasonable reference: {}".format(referenceName))
            transformedSample = np.dot(centeredSample, rotation.transpose()) + translation
            maskedSample = transformedSample[matchMask]
            fitnessComputer = AbsoluteNeighborFitnessComputer(maskedSample, self._tolerance)
            fitness = fitnessComputer.compute(self._referenceClouds[referenceName])
            print("Fitess: {}".format(fitness))
            if fitness < bestFitness:
                bestFitness = fitness
                self._bestReferenceName = referenceName
                self._bestTransformation = (scale, rotation, translation)
                print("referenceName: {}".format(referenceName))
                print("matched. bestFitness: {}".format(fitness))
                print("               scale: {}".format(scale))
                print("         translation: {}".format(translation))
                print("            rotation: {}".format(rotation))

        return self._bestReferenceName

    def getImageRepresentation(self):
        print("getImageRepresentation:", self._bestReferenceName)
        text = self._bestReferenceName
        size = 100
        canvas = Image.new("RGB", [size, size], (255, 255, 255))
        draw = ImageDraw.Draw(canvas)
        textWidth, textHeight = draw.textsize(text)
        offset = (5, 5)
        white = "#000000"
        draw.text(offset, text, fill=white)
        ret = 255.0 - np.asarray(canvas)

        middleOfImage = np.array([[50.0, 50.0]])

        cloudPoints = np.dot(self._lastCloud, self._bestTransformation[1].transpose()) + self._bestTransformation[2] + middleOfImage

        referencePoints = self._referenceClouds[self._bestReferenceName] + middleOfImage

        ImageUtilities.addPointsToImage(ret, cloudPoints, 0)
        ImageUtilities.addPointsToImage(ret, referencePoints, 1)

        return ret

    def __ne__(self, other):
        if type(self) != type(other):
            return True

        # TODO: dont do pointer comparison here.
        return self._matchers != other._matchers


def getMatchMask(sample, reference, tolerance):
    squareDistances = PointUtilities.computeSquareDistances(sample, reference)
    fromSampleClosestNeighbor = np.min(squareDistances, axis=1)
    return fromSampleClosestNeighbor < tolerance
