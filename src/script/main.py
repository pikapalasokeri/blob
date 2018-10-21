#!/usr/bin/python3
import ImageGrabber
import ResultHandler
import JsonPipelineParser
import json
import sys
import argparse


def _parseCommandLine(commandLine):
    parser = argparse.ArgumentParser("Main program for dice mining.")
    parser.add_argument("--image_grabber", type=str, default="", help="Image grabber json definition.", required=True)
    parser.add_argument("--pipeline", type=str, default="", help="Image processing pipeline json definition.", required=True)
    parser.add_argument("--result_handler", type=str, default="", help="Result handler json definition.")

    args = parser.parse_args()
    return args


def _createImageProcessingPipeline(jsonPath):
    with open(jsonPath) as f:
        definition = json.loads("".join(f.readlines()))
        return JsonPipelineParser.jsonToPipeline(definition)


if __name__ == "__main__":
    commandLineArguments = _parseCommandLine(sys.argv)
    imageGrabber = ImageGrabber.createImageGrabber(commandLineArguments.image_grabber)
    imageProcessingPipeline = _createImageProcessingPipeline(commandLineArguments.pipeline)
    resultHandler = ResultHandler.createResultHandler(commandLineArguments.result_handler)

    for image in imageGrabber.grab():
        result = imageProcessingPipeline.execute(image.image)
        resultHandler.handleResult(image, result)
