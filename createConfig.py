#!/usr/bin/python

from ConfigCreator import ConfigCreator
from FileImageReader import FileImageReader

imageReader = FileImageReader("images/early_tests_white_01.config")
#imageReader = FileImageReader()
creator = ConfigCreator(imageReader)

creator.readImages()
creator.calibrateEdgeDetection()
