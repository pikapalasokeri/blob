import json


class ResultHandler:
    def handleResult(self, image, result):
        raise NotImplementedError("Class {} doesn't implement handleResult().".format(self.__class__.__name__))


class PrintResultHandler(ResultHandler):
    def handleResult(self, image, result):
        print("{} classified as {}".format(image.comment, str(result)))


def createResultHandler(jsonPath):
    with open(jsonPath) as f:
        definition = json.loads("".join(f.readlines()))
    type = definition["type"]
    if type == "Print":
        return PrintResultHandler()
    else:
        raise Exception("{} is not a valid result handler.".format(type))
