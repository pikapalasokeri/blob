#!/bin/bash
echo "Running swig unit tests..."
export PYTHONPATH=`pwd`"/../../main/swig:$1:$2"
echo $PYTHONPATH
python3 -m unittest -v \
       TestMostPopulatedCircleFinder\
       TestCoherentPointDriftMatcher2D\
       TestSimulatedAnnealingPointMatcher2D\
       TestEdgeDetector\
       TestAbsoluteNeighborFitnessComputer\
       TestPointCloudHandler
