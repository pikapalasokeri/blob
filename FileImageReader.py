from ReferenceImage import ReferenceImage
from scipy import misc


def _getKeyboardInputNext():
    inputStr = raw_input("Path to image (leave empty when done): ")
    if not inputStr:
        return None
    
    filePath = inputStr
    comment = raw_input("Comment: ")
    return ReferenceImage(misc.imread(filePath), comment)


class FileImageReader:
    def __init__(self, configFile = None):
        self._imagesFromConfigFile = []
        self._indexInConfigFileImages = 0
        if configFile is not None:
            with open(configFile) as config:
                for line in config:
                    filePath = line.strip()
                    self._imagesFromConfigFile.append(ReferenceImage(misc.imread(filePath), filePath))
    
    def getNext(self):
        if len(self._imagesFromConfigFile) == 0:
            return _getKeyboardInputNext()
        else:
            return self._getNextInConfigFile()


    def _getNextInConfigFile(self):
        if self._indexInConfigFileImages == len(self._imagesFromConfigFile):
            return None

        self._indexInConfigFileImages += 1
        return self._imagesFromConfigFile[self._indexInConfigFileImages-1]


