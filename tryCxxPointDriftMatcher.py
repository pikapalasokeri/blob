#!/usr/bin/python

from cxx.CxxPointMatcher import CxxCoherentPointDriftMatcher2D

testObject = CxxCoherentPointDriftMatcher2D()
testObject.addPoint1(1.0, 2.123124)
testObject.addPoint2(-1234.1234, 0.0)
testObject.addPoint2(-1234.1234, 12341234)
testObject.output()
testObject.match()