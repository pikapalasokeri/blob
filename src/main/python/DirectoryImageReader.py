from ReferenceImage import ReferenceImage
import imageio
import os


class DirectoryImageReader:
    supportedExtensions = [".jpg"]

    def __init__(self, directory):
        self._filePaths = []
        for f in os.listdir(directory):
            filePath = os.path.join(directory, f)
            if os.path.isfile(filePath):
                fileParts = os.path.splitext(f)
                extension = fileParts[1]
                if extension in self.supportedExtensions:
                    self._filePaths.append(filePath)

    def generate(self):
        for filePath in self._filePaths:
            comment = os.path.basename(filePath)
            yield ReferenceImage(imageio.imread(filePath), comment)
