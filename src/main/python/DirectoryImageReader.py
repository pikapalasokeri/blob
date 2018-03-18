from ReferenceImage import ReferenceImage
from scipy import misc
import os

class DirectoryImageReader:
    supportedExtensions = [".jpg"]

    def __init__(self, directory):
        self._filePaths = []
        for f in os.listdir(directory):
            filePath = os.path.join(directory, f)
            if os.path.isfile(filePath):
                fileParts = os.path.splitext(f)
                name = fileParts[0]
                extension = fileParts[1]
                if extension in self.supportedExtensions:
                    self._filePaths.append(filePath)


    def generate(self):
        for filePath in self._filePaths:
            comment = os.path.basename(filePath)
            yield ReferenceImage(misc.imread(filePath), comment)
