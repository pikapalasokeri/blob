from ctypes import cdll
lib = cdll.LoadLibrary('./cxx/build/libpointmatcher.so')

class CxxCoherentPointDriftMatcher2D(object):
  def __init__(self):
    self.obj = lib.CoherentPointDriftMatcher2D_new()

  def __del__(self):
    lib.CoherentPointDriftMatcher2D_delete(self.obj)
