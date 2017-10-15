from Classifier import Classifier
from EdgeDetectionConfig import EdgeDetectionConfig
from FileImageReader import FileImageReader

config = EdgeDetectionConfig(2.2, 6.5, 30, 1.0)
referenceImageReader = FileImageReader("images/early_tests_white_01.config")
referenceImages = [x for x in referenceImageReader.generate()]

classifier = Classifier(config, referenceImages)

# just try to classify the references as sanity check.
totalTries = 0
numCorrect = 0
allImagesReader = FileImageReader("images/early_tests_white_all.config")
for image in allImagesReader.generate():
    classified = classifier.classify(image)
    if classified is not None:
        firstPart = image.comment.split("_")[-2]
        secondPart = classified.comment.split("_")[-2]
        if firstPart == secondPart:
            correct = True
            numCorrect += 1
        else:
            correct = False
        print "     Classified", image.comment, "as", classified.comment, "   ", correct
    else:
        print "     Completely failed to classify", image.comment
    totalTries += 1
    print ""




print "Total tries:", totalTries
print "Correct classifications:", numCorrect
