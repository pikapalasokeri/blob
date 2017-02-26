from ReferenceImage import ReferenceImage
from scipy import misc

class FileImageReader:
    def getNext(self):
        inputStr = raw_input("Path to image (leave empty when done): ")
        if not inputStr:
            return None
        
        filePath = inputStr
        comment = raw_input("Comment: ")
        return ReferenceImage(misc.imread(filePath), comment)
