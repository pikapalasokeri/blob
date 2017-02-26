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
  sigma = 1
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

  for ix, sigma in enumerate([16]):#, 2, 4, 8, 16, 32, 64]):
    print "sigma", sigma
    extremas = BlobDetection.detectBlobs(compensatedGaussImg, sigma)
    print extremas
    baseRadius = sigma*1.4142*0.0

    circleColor = np.max(compensatedGaussImg)
    for extrema in zip(extremas[0], extremas[1]):
      X = np.cos(np.linspace(0.0, 2*np.pi, 314))
      Y = np.sin(np.linspace(0.0, 2*np.pi, 314))
      for tx, ty in zip(X,Y):
        for radius in np.linspace(baseRadius, baseRadius+1, 1):
          col = int(round(tx*radius)) + extrema[1]
          row = int(round(ty*radius)) + extrema[0]
          if (col < compensatedGaussImg.shape[1] and col >= 0 and row < compensatedGaussImg.shape[0] and row >= 0):
            compensatedGaussImg[row,col] = 100

    #plt.subplot(3, 3, ix+1)
  print "plotting..."
  plt.figure(5)
  plt.imshow(compensatedGaussImg)

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
  