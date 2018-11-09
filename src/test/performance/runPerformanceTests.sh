#!/bin/bash
export PYTHONPATH=`pwd`"/../../main/swig:$1:$2"
echo $PYTHONPATH
python3 -m unittest -v \
       TestBruteForceMatcherPerformance
