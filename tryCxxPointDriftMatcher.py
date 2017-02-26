#!/usr/bin/python

from cxx.CxxPointMatcher import CxxCoherentPointDriftMatcher2D
from CoherentPointDriftMatcher import CoherentPointDriftMatcher2D
import numpy as np

pointSet1 = np.array([[1.0, 2.123124],
                      [2.0, 2.0]])

pointSet2 = []
#pointSet2.append((-1234.1234, 0.0))
#pointSet2.append((-1234.1234, 12341234))
pointSet2 = np.array([[-12.1234, 0.0],
                      [-12.1234, 4.0]])

referenceObject = CoherentPointDriftMatcher2D(pointSet1, pointSet2)
referenceObject.match(0.0)

print "------------------------------------------------"



testObject = CxxCoherentPointDriftMatcher2D()
for p in pointSet1:
    testObject.addPoint1(p[0], p[1])

for p in pointSet2:
    testObject.addPoint2(p[0], p[1])

testObject.output()
m = testObject.match()
print "Done matching. Back in python."
print m
