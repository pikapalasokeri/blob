#!/usr/bin/python3

from ConfigCreator import ConfigCreator
from FileImageReader import FileImageReader
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: " + sys.argv[0] + " referencelist")
        print("  where referenlist is a file containing paths to the reference images.")
        exit(0)

    referenceListPath = sys.argv[1]
    imageReader = FileImageReader(referenceListPath)
    creator = ConfigCreator(imageReader)

    creator.readImages()
    creator.calibrateEdgeDetection()
