from ctypes import *
lib = cdll.LoadLibrary('./cxx/build/libpointmatcher.so')

class CxxCoherentPointDriftMatcher2D(object):
  def __init__(self):
    self.obj = lib.CoherentPointDriftMatcher2D_new()

  def __del__(self):
    lib.CoherentPointDriftMatcher2D_delete(self.obj)

  def addPoint1(self, x, y):
    lib.CoherentPointDriftMatcher2D_addPoint1(self.obj, c_double(x), c_double(y))

  def addPoint2(self, x, y):
    lib.CoherentPointDriftMatcher2D_addPoint2(self.obj, c_double(x), c_double(y))

  def match(self):
    lib.CoherentPointDriftMatcher2D_match(self.obj)
