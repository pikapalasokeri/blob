#!/usr/bin/python3
from Classifier import Classifier
from EdgeDetectionConfig import EdgeDetectionConfig
from FileImageReader import FileImageReader
import sys
import argparse


def _parseCommandLine(commandLine):
    parser = argparse.ArgumentParser("Main program for dice mining.")
    parser.add_argument("--edge_sigma", type=float, default=2.2, help="Sigma (edge detection)")
    parser.add_argument("--edge_threshold", type=float, default=6.5, help="Threshold factor (edge detection)")
    parser.add_argument("--edge_radius", type=float, default=30, help="Radius beyond which to discard points (edge detection)")
    parser.add_argument("--edge_keepfactor", type=float, default=0.5, help="Fraction of edge points to keep (0.0, 1.0] (edge detection)")

    parser.add_argument("reference_reader", type=str, default="", help="Argument to reference reader. Supported values: FileImageReader:<path to config>")
    parser.add_argument("image_reader", type=str, default="", help="Argument to image reader. Supported values: file_early_tests_white_all")

    args = parser.parse_args()
    return args


def _getEdgeDetectionConfig(commandLineArguments):
    return EdgeDetectionConfig(commandLineArguments.edge_sigma,
                               commandLineArguments.edge_threshold,
                               commandLineArguments.edge_radius,
                               commandLineArguments.edge_keepfactor)


def _getReferenceImageCreator(commandLineArguments):
    argumentString = commandLineArguments.reference_reader

    tokens = argumentString.split(":")
    if tokens[0] == "FileImageReader":
        return FileImageReader(tokens[1])
    else:
        raise Exception("Reference image reader argument is not supported.")


def _getImageCreator(commandLineArguments):
    argumentString = commandLineArguments.image_reader

    tokens = argumentString.split(":")
    if tokens[0] == "FileImageReader":
        return FileImageReader(tokens[1])
    else:
        raise Exception("Image reader argument is not supported.")

if __name__ == "__main__":
    commandLineArguments = _parseCommandLine(sys.argv)
    edgeDetectionConfig = _getEdgeDetectionConfig(commandLineArguments)
    referenceImageReader = _getReferenceImageCreator(commandLineArguments)
    imageCreator = _getImageCreator(commandLineArguments)

    referenceImages = [x for x in referenceImageReader.generate()]
    classifier = Classifier(edgeDetectionConfig, referenceImages)
    for image in imageCreator.generate():
        classifiedImage = classifier.classify(image)
        print("Got image", image)
        print("Classified as", classifiedImage)
