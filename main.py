#!/usr/bin/python

from scipy import misc
from scipy import ndimage
import numpy as np
import matplotlib.pyplot as plt

def rgb2gray(img):
  return np.dot(img[...,:3], [1.0/3.0, 1.0/3.0, 1.0/3.0])

def findCenterOfMass(mask):
    indices = np.nonzero(mask)
    centerOfMassRows = np.sum(indices[0])
    centerOfMassCols = np.sum(indices[1])
    return (centerOfMassRows/indices[0].size, centerOfMassCols/indices[1].size)

def getBlobs(filePath, backgroundPath):
  img = misc.imread(filePath)
  bgImg = misc.imread(backgroundPath)
  grayImg = rgb2gray(img)
  bgGrayImg = rgb2gray(bgImg)
  sigma = 16
  gaussImg = ndimage.gaussian_filter(grayImg, sigma)
  bgGaussImg = ndimage.gaussian_filter(bgGrayImg, sigma)
  compensatedGaussImg = gaussImg - bgGaussImg

  mask = compensatedGaussImg < 0.5*np.mean(compensatedGaussImg)
  centerOfMass = findCenterOfMass(mask)
  print "center of mass:", centerOfMass

  plt.figure(1)
  plt.subplot(1,2,1)
  plt.imshow(img)
  plt.subplot(1,2,2)
  plt.imshow(bgImg)

  plt.figure(2)
  plt.imshow(compensatedGaussImg)
  
  plt.figure(4)
  plt.imshow(mask)
  
  log = ndimage.gaussian_laplace(compensatedGaussImg, 8)
  log = np.absolute(log)
  threshold = np.max(log)*0.5
  print threshold
  potentialExtremas = np.nonzero(log > threshold)
  extremas = []
  for row, col in zip(potentialExtremas[0], potentialExtremas[1]):
    value = log[row, col]
    isExtrema = True
    for r in range(row-1, row+2):
      for c in range(col-1, col+2):
        if r == row and c == col:
          continue
        if log[r,c] >= value: 
          isExtrema = False
    if isExtrema:
      extremas.append((row, col))

  print extremas
  radius = sigma*1.4142

  for extrema in extremas:
    X = np.cos(np.linspace(0.0, 2*np.pi, 324))
    Y = np.sin(np.linspace(0.0, 2*np.pi, 324))
    for tx, ty in zip(X,Y):
      col = int(round(tx*radius)) + extrema[1]
      row = int(round(ty*radius)) + extrema[0]
      log[row,col] = threshold

  plt.figure(5)
  plt.imshow(log)

  '''
  log = ndimage.gaussian_laplace(compensatedGaussImg, 16)
  plt.figure(6)
  plt.imshow(log)

  log = ndimage.gaussian_laplace(compensatedGaussImg, 32)
  plt.figure(7)
  plt.imshow(log)

  log = ndimage.gaussian_laplace(compensatedGaussImg, 64)
  plt.figure(8)
  plt.imshow(log)
  '''



  plt.show()

if __name__ == "__main__":
  getBlobs("images/1.jpg", "images/1bg.jpg")
  