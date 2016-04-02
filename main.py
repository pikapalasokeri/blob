#!/usr/bin/python

from scipy import misc
import numpy as np

def rgb2gray(img):
  return np.dot(img[...,:3], [1.0/3.0, 1.0/3.0, 1.0/3.0])

def getBlobs(filePath):
  img = misc.imread(filePath)
  grayImg = rgb2gray(img)
  

if __name__ == "__main__":
  getBlobs("images/1.jpg")
  