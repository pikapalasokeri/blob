#!/usr/bin/python

from ConfigCreator import ConfigCreator
from FileImageReader import FileImageReader

imageReader = FileImageReader()
creator = ConfigCreator(imageReader)

creator.readImages()
creator.calibrateEdgeDetection()
