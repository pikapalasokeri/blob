#!/usr/bin/python3

from scipy import misc
from scipy import ndimage
import numpy as np
import matplotlib.pyplot as plt
from EdgeDetector import *

def addEdgesToImage(image, edges, colorIx):
  for row, col in zip(edges[0], edges[1]):
    image[row, col, colorIx] = 255

if __name__ == "__main__":
  filePath = "images/TryEdgeDetector.jpg"
  img = misc.imread(filePath)
  edgeDetector = EdgeDetector(img)

  sigma = 4
  thresholdFactor = 0.4
  edges = edgeDetector.getEdges(sigma, thresholdFactor)
  print("Got", len(edges[0]), "edge points at sigma", sigma, "and thresholdFactor", thresholdFactor)
  addEdgesToImage(img, edges, 0)
  addEdgesToImage(img, edges, 2)

  sigma = 8
  thresholdFactor = 0.1
  edges = edgeDetector.getEdges(sigma, thresholdFactor)
  print("Got", len(edges[0]), "edge points at sigma", sigma, "and thresholdFactor", thresholdFactor)
  addEdgesToImage(img, edges, 1)

  sigma = 16
  thresholdFactor = 0.01
  edges = edgeDetector.getEdges(sigma, thresholdFactor)
  print("Got", len(edges[0]), "edge points at sigma", sigma, "and thresholdFactor", thresholdFactor)  
  addEdgesToImage(img, edges, 2)

  plt.figure()
  plt.imshow(img)
  plt.show()
