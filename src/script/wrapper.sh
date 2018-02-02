#!/bin/bash
export PYTHONPATH="$PWD/python:$PWD/lib"
export LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:$PWD/lib"
exec $@
