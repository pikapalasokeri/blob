import numpy as np
from EdgeDetector import EdgeDetector
from SimulatedAnnealingPointMatcher2D import SimulatedAnnealingPointMatcher2D
from MeanShortestDistanceFitnessComputer import MeanShortestDistanceFitnessComputer
from PointCloud import PointCloud
from ImageUtilities import rgb2grayNaive
import PipelineStage


class Classifier:
    def __init__(self, edgeDetectionConfig, references):
        self._references = references
        self._edgeDetectionConfig = edgeDetectionConfig
        self._referenceEdges = [self._detectEdges(x) for x in references]

    def classify(self, image):
        edgesToClassify = self._detectEdges(image)
        bestScore = float("Inf")
        currentGuess = None
        print(image.comment)
        for refEdges, reference in zip(self._referenceEdges, self._references):
            score = _getLikenessScore(refEdges, edgesToClassify)

            print("    ", reference.comment, "   ", score)
            if score is None:
                continue

            if score < bestScore:
                bestScore = score
                currentGuess = reference
        return currentGuess

    def _detectEdges(self, image):
        edgeDetector = EdgeDetector(rgb2grayNaive(image.image))
        edges = edgeDetector.getEdges(self._edgeDetectionConfig.sigma,
                                      self._edgeDetectionConfig.thresholdFactor)
        keepInsideStage = PipelineStage.KeepInsideRadiusStage(self._edgeDetectionConfig.radius)
        edges = keepInsideStage.execute(edges)
        trimmedEdges = self._trimEdges(edges)
        return _convertToMatrix(trimmedEdges)

    '''
    I really don't know why this method works so well, except for threshold 0.8 or 0.2,
    but I'm keeping it since it seems to work very well for everything else,
    and 0.8 and 0.2 are off by 2 at most.
    '''
    def _trimEdges(self, cloud):
        newCloud = PointCloud()

        keepThreshold = self._edgeDetectionConfig.keepFactor
        accumulatedKeep = 0.0
        accumulatedKeepCorrection = 0.0
        for point in cloud:
            if accumulatedKeep - accumulatedKeepCorrection < keepThreshold:
                newCloud.addPoint(point)
        accumulatedKeep += keepThreshold

        if accumulatedKeep - accumulatedKeepCorrection >= 1.0:
            accumulatedKeepCorrection += 1.0

        return newCloud


def _convertToMatrix(points):
    newPoints = np.zeros((points.size(), 2))
    for ix, point in enumerate(points):
        newPoints[ix, 0] = point[0]
        newPoints[ix, 1] = point[1]
    return newPoints


def _getLikenessScore(reference, edgesToClassify):
    referenceCenter = np.mean(reference, axis=0)
    edgesToClassifyCenter = np.mean(edgesToClassify, axis=0)
    centeredReference = reference - referenceCenter
    centeredEdgesToClassify = edgesToClassify - edgesToClassifyCenter

    fitnessComputer = MeanShortestDistanceFitnessComputer(centeredReference)
    matcher = SimulatedAnnealingPointMatcher2D(fitnessComputer)
    matcher.setNumIterations(2000)

    for p in centeredEdgesToClassify:
        matcher.addPoint(p[0], p[1])

    scale, rotation, translation, fitness = matcher.match()
    if scale < 0.8 or scale > 1.2:
        return None

    return fitness
