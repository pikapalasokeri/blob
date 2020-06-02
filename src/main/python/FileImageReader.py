from ReferenceImage import ReferenceImage
import imageio


class FileImageReader:
    def __init__(self, configFile=None):
        self._imagesFromConfigFile = []
        self._indexInConfigFileImages = 0
        if configFile is not None:
            with open(configFile) as config:
                for line in config:
                    filePath = line.strip()
                    self._imagesFromConfigFile.append(ReferenceImage(imageio.imread(filePath), filePath))

    def generate(self):
        if len(self._imagesFromConfigFile) == 0:
            inputStr = input("Path to image (leave empty when done): ")
            while inputStr:
                filePath = inputStr
                comment = input("Comment: ")
                inputStr = input("Path to image (leave empty when done): ")
                yield ReferenceImage(imageio.imread(filePath), comment)
        else:
            for referenceImage in self._imagesFromConfigFile:
                yield referenceImage
