from ReferenceImage import ReferenceImage
from scipy import misc

class FileImageReader:
    def __init__(self, configFile = None):
        self._imagesFromConfigFile = []
        self._indexInConfigFileImages = 0
        if configFile is not None:
            with open(configFile) as config:
                for line in config:
                    filePath = line.strip()
                    self._imagesFromConfigFile.append(ReferenceImage(misc.imread(filePath), filePath))

    def generate(self):
        if len(self._imagesFromConfigFile) == 0:
            inputStr = raw_input("Path to image (leave empty when done): ")
            while inputStr:
                filePath = inputStr
                comment = raw_input("Comment: ")
                inputStr = raw_input("Path to image (leave empty when done): ")
                yield ReferenceImage(misc.imread(filePath), comment)
        else:
            for referenceImage in self._imagesFromConfigFile:
                yield referenceImage
