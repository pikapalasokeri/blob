from ctypes import *
from numpy.ctypeslib import ndpointer
lib = cdll.LoadLibrary('./cxx/build/libcxxblob.so')

class CxxMostPopulatedCircleFinder(object):
    def __init__(self, points):
        self.obj = lib.MostPopulatedCircleFinder_new()

        cxxFunction = lib.MostPopulatedCircleFinder_addPoint
        cxxFunction.restype = None
        cxxFunction.argtypes = [c_void_p, c_double, c_double]
        for x, y in zip(points[0], points[1]):
            cxxFunction(self.obj, x, y)

    def __del__(self):
        lib.MostPopulatedCircleFinder_delete(self.obj)

    def findCircle(self, radius):
        cxxFunction = lib.MostPopulatedCircleFinder_get
        cxxFunction.restype = c_bool
        cxxFunction.argtypes = [c_void_p, c_double, POINTER(c_double), POINTER(c_double)]
        resultX = c_double()
        resultY = c_double()
        success = cxxFunction(self.obj, radius, byref(resultX), byref(resultY))
        if success:
            return (resultX.value, resultY.value)
        else:
            return None
