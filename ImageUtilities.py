import numpy as np

def rgb2grayNaive(img):
  return np.dot(img[...,:3], [1.0/3.0, 1.0/3.0, 1.0/3.0])
