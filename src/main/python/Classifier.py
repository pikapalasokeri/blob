import numpy as np
from EdgeDetector import EdgeDetector
from SimulatedAnnealingPointMatcher2D import SimulatedAnnealingPointMatcher2D
from MeanShortestDistanceFitnessComputer import MeanShortestDistanceFitnessComputer
from CoherentPointDriftMatcher import transform

class Classifier:
    def __init__(self, edgeDetectionConfig, references):
        self._references = references
        self._edgeDetectionConfig = edgeDetectionConfig
        self._referenceEdges = [self._detectEdges(x) for x in references]

    def classify(self, image):
        edgesToClassify = self._detectEdges(image)
        bestScore = float("Inf")
        currentGuess = None
        print image.comment
        for refEdges, reference in zip(self._referenceEdges, self._references):
            score = _getLikenessScore(refEdges, edgesToClassify)

            print "    ", reference.comment, "   ", score
            if score is None:
                continue

            if score < bestScore:
                bestScore = score
                currentGuess = reference
        return currentGuess

    def _detectEdges(self, image):
        edgeDetector = EdgeDetector(image.image)
        edges = edgeDetector.getEdges(self._edgeDetectionConfig.sigma,
                                      self._edgeDetectionConfig.thresholdFactor,
                                      self._edgeDetectionConfig.radius)

        trimmedEdges = self._trimEdges(edges)
        return _convertToMatrix(trimmedEdges)

    '''
    I really don't know why this method works so well, except for threshold 0.8 or 0.2,
    but I'm keeping it since it seems to work very well for everything else,
    and 0.8 and 0.2 are off by 2 at most.
    '''
    def _trimEdges(self, points):
        newPoints = []

        keepThreshold = self._edgeDetectionConfig.keepFactor
        accumulatedKeep = 0.0
        accumulatedKeepCorrection = 0.0
        for point in points:
            if accumulatedKeep-accumulatedKeepCorrection < keepThreshold:
                newPoints.append(point)
        accumulatedKeep += keepThreshold

        if accumulatedKeep - accumulatedKeepCorrection >= 1.0:
            accumulatedKeepCorrection += 1.0

        return newPoints

def _convertToMatrix(points):
    newPoints = np.zeros((len(points[0]), 2))
    for ix in range(len(points[0])):
        newPoints[ix, 0] = points[0][ix]
        newPoints[ix, 1] = points[1][ix]
    return newPoints

def _getLikenessScore(reference, edgesToClassify):
    referenceCenter = np.mean(reference, axis = 0)
    edgesToClassifyCenter = np.mean(edgesToClassify, axis = 0)
    centeredReference = reference - referenceCenter
    centeredEdgesToClassify = edgesToClassify - edgesToClassifyCenter

    fitnessComputer = MeanShortestDistanceFitnessComputer(centeredReference)
    matcher = SimulatedAnnealingPointMatcher2D(fitnessComputer)
    matcher.setNumIterations(2000)

    for p in centeredEdgesToClassify:
        matcher.addPoint1(p[0], p[1])

    scale, rotation, translation = matcher.match()
    if scale < 0.8 or scale > 1.2:
        return None

    transformed = transform(scale, rotation, translation, centeredEdgesToClassify)
    return _computeClosestNeighborLikeness(centeredReference, transformed)

def _computeClosestNeighborLikeness(points1, points2):
    squareDistances = _computeSquareDistances(points1, points2)
    from1ClosestNeighbor = np.min(squareDistances, axis=1)
    from2ClosestNeighbor = np.min(squareDistances, axis=0)
    return np.mean(from1ClosestNeighbor) + np.mean(from2ClosestNeighbor)

def _computeSquareDistances(points1, points2):
    numPoints1 = points1.shape[0]
    numPoints2 = points2.shape[0]

    squareDistances = np.zeros((numPoints1, numPoints2))
    for i, point1 in enumerate(points1):
        for j, point2 in enumerate(points2):
            squareDistances[i,j] = _computeSquareDistance(point1, point2)
    return squareDistances

def _computeSquareDistance(point1, point2):
    diff = point1 - point2
    return float(diff[0]**2 + diff[1]**2)
