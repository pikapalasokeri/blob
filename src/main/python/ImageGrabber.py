import json
import os
import imageio


class Image:
    def __init__(self, image, comment):
        self.image = image
        self.comment = comment


class ImageGrabber:
    def grab(self):
        raise NotImplementedError("Class {} doesn't implement grab().".format(self.__class__.__name__))


class DirectoryImageGrabber(ImageGrabber):
    def __init__(self, definition):
        self._directory = definition["directory"]
        self._allowedExtensions = ["." + ext for ext in definition["extensions"].strip().split(",")]

    def grab(self):
        for (dirpath, dirnames, filenames) in os.walk(self._directory):
            for filename in filenames:
                print(filename)
                _, extension = os.path.splitext(filename)
                if extension in self._allowedExtensions:
                    filePath = os.path.join(dirpath, filename)
                    comment = filename
                    print("yielding... {}, {}".format(comment, filePath))
                    yield Image(imageio.imread(filePath), comment)


def createImageGrabber(jsonPath):
    with open(jsonPath) as f:
        definition = json.loads("".join(f.readlines()))

    type = definition["type"]
    if type == "DirectoryImageGrabber":
        return DirectoryImageGrabber(definition)
    else:
        raise Exception("{} not a valid image grabber".format(type))
