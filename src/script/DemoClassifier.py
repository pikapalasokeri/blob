#!/usr/bin/python3

from Classifier import Classifier
from EdgeDetectionConfig import EdgeDetectionConfig
from FileImageReader import FileImageReader
import sys
import os


def runDemo():
    config = EdgeDetectionConfig(2, 2, 41, 1.0)
    # referenceImageReader = FileImageReader("../demoseries/clean_demo_series_6_crop.config")
    home = os.getenv("HOME")
    referenceImageReader = FileImageReader(home + "/demoseries/clean_demo_series_6_crop_small.config")
    referenceImages = [x for x in referenceImageReader.generate()]
    print("Reference images generated.")

    classifier = Classifier(config, referenceImages)
    print("Classifier created.")

    # just try to classify the references as sanity check.
    totalTries = 0
    numCorrect = 0
    allImagesReader = FileImageReader(home + "/demoseries/clean_demo_series_6_crop.config")
    # allImagesReader = FileImageReader("../demoseries/clean_demo_series_6_crop_small.config")
    for image in allImagesReader.generate():
        classified = classifier.classify(image)

        if classified is not None:
            firstFileName = image.comment.split("/")[-1]
            firstPart = firstFileName.split("_")[0]
            secondFileName = classified.comment.split("/")[-1]
            secondPart = secondFileName.split("_")[0]
            if firstPart == secondPart:
                correct = True
                numCorrect += 1
            else:
                correct = False
            print("     Classified", image.comment, "as", classified.comment, "   ", correct)
        else:
            print("     Completely failed to classify", image.comment)
        totalTries += 1
        print("")

    print("Total tries:", totalTries)
    print("Correct classifications:", numCorrect)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        runDemo()
    elif sys.argv[1] == "profile":
        print("Running through cProfile...")
        import cProfile
        cProfile.run(runDemo())
    else:
        "Unrecognized argument."
