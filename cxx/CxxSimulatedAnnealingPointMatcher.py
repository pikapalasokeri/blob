from ctypes import *
from numpy.ctypeslib import ndpointer
import numpy
lib = cdll.LoadLibrary('./cxx/build/libpointmatcher.so')

class CxxSimulatedAnnealingPointMatcher2D(object):
    def __init__(self):
        self.obj = lib.SimulatedAnnealingPointMatcher2D_new()

    def __del__(self):
        lib.SimulatedAnnealingPointMatcher2D_delete(self.obj)

    def addPoint1(self, x, y):
        cxxFunction = lib.SimulatedAnnealingPointMatcher2D_addPoint1
        cxxFunction.restype = None
        cxxFunction.argtypes = [c_void_p, c_double, c_double]
        cxxFunction(self.obj, x, y)

    def addPoint2(self, x, y):
        cxxFunction = lib.SimulatedAnnealingPointMatcher2D_addPoint2
        cxxFunction.restype = None
        cxxFunction.argtypes = [c_void_p, c_double, c_double]
        cxxFunction(self.obj, x, y)

    def setNumIterations(self, numIterations):
        cxxFunction = lib.SimulatedAnnealingPointMatcher2D_setNumIterations
        cxxFunction.restype = None
        cxxFunction.argtypes = [c_void_p, c_int]
        cxxFunction(self.obj, numIterations)

    def setStartTemperature(self, temperature):
        cxxFunction = lib.SimulatedAnnealingPointMatcher2D_setStartTemperature
        cxxFunction.restype = None
        cxxFunction.argTypes = [c_void_p, c_double]
        cxxFunction(self.obj, c_double(temperature))

    def setInitialRotationSigma(self, rotationSigma):
        cxxFunction = lib.SimulatedAnnealingPointMatcher2D_setInitialRotationSigma
        cxxFunction.restype = None
        cxxFunction.argTypes = [c_void_p, c_double]
        cxxFunction(self.obj, c_double(rotationSigma))

    def setSlowRotationSigma(self, rotationSigma):
        cxxFunction = lib.SimulatedAnnealingPointMatcher2D_setSlowRotationSigma
        cxxFunction.restype = None
        cxxFunction.argTypes = [c_void_p, c_double]
        cxxFunction(self.obj, c_double(rotationSigma))

    def setInitialTranslationSigma(self, translationSigma):
        cxxFunction = lib.SimulatedAnnealingPointMatcher2D_setInitialTranslationSigma
        cxxFunction.restype = None
        cxxFunction.argTypes = [c_void_p, c_double]
        cxxFunction(self.obj, c_double(translationSigma))

    def setSlowTranslationSigma(self, translationSigma):
        cxxFunction = lib.SimulatedAnnealingPointMatcher2D_setSlowTranslationSigma
        cxxFunction.restype = None
        cxxFunction.argTypes = [c_void_p, c_double]
        cxxFunction(self.obj, c_double(translationSigma))

    def setSlowMovementBreakpoint(self, breakpoint):
        cxxFunction = lib.SimulatedAnnealingPointMatcher2D_setSlowMovementBreakpoint
        cxxFunction.restype = None
        cxxFunction.argTypes = [c_void_p, c_double]
        cxxFunction(self.obj, c_double(breakpoint))

    def setVerbose(self, verbose):
        cxxFunction = lib.SimulatedAnnealingPointMatcher2D_setVerbose
        cxxFunction.restype = None
        cxxFunction.argtypes = [c_void_p, c_bool]
        cxxFunction(self.obj, verbose)

    def setNumThreads(self, numThreads):
        cxxFunction = lib.SimulatedAnnealingPointMatcher2D_setNumThreads
        cxxFunction.restype = None
        cxxFunction.argtypes = [c_void_p, c_int]
        cxxFunction(self.obj, numThreads)

    def match(self):
        cxxFunction = lib.SimulatedAnnealingPointMatcher2D_match
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
        cxxFunction = lib.SimulatedAnnealingPointMatcher2D_output
        cxxFunction.restype = None
        cxxFunction(self.obj)
