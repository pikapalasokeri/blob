from ctypes import *
from numpy.ctypeslib import ndpointer
import numpy
lib = cdll.LoadLibrary('./cxx/build/libpointmatcher.so')

class CxxCoherentPointDriftMatcher2D(object):
  def __init__(self):
    self.obj = lib.CoherentPointDriftMatcher2D_new()

  def __del__(self):
    lib.CoherentPointDriftMatcher2D_delete(self.obj)

  def addPoint1(self, x, y):
    cxxFunction = lib.CoherentPointDriftMatcher2D_addPoint1
    cxxFunction.restype = None
    # This c_void_p here feels shaky. In case of weird core dumps, look here.
    cxxFunction.argtypes = [c_void_p, c_double, c_double]
    cxxFunction(self.obj, x, y)

  def addPoint2(self, x, y):
    cxxFunction = lib.CoherentPointDriftMatcher2D_addPoint2
    cxxFunction.restype = None
    cxxFunction.argtypes = [c_void_p, c_double, c_double]
    cxxFunction(self.obj, x, y)

  def match(self):
    cxxFunction = lib.CoherentPointDriftMatcher2D_match
    cxxFunction.restype = None
    cxxFunction.argtypes = [c_void_p, \
                            ndpointer(c_double, flags="C_CONTIGUOUS"), \
                            ndpointer(c_double, flags="C_CONTIGUOUS"), \
                            ndpointer(c_double, flags="C_CONTIGUOUS")]
    scale = numpy.zeros((1, 1))
    rotation = numpy.zeros((2, 2))
    translation = numpy.zeros((1, 2))
    cxxFunction(self.obj, scale, rotation, translation)
    return scale[0, 0], rotation, translation

  def output(self):
    cxxFunction = lib.CoherentPointDriftMatcher2D_output
    cxxFunction.restype = None
    cxxFunction(self.obj)
