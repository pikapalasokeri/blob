#!/bin/bash

python -m unittest -v \
       TestEdgeDetector\
       TestCxxCoherentPointDriftMatcher2D\
       TestCxxSimulatedAnnealingPointMatcher2D\
       TestCxxMostPopulatedCircleFinder
