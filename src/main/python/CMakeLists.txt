cmake_minimum_required (VERSION 3.5)
project (blob_src_main_python)

set(PROJECT_SOURCE_DIR .)

install(FILES Classifier.py
              CoherentPointDriftMatcher.py
              ConfigCreator.py
              EdgeDetectionConfig.py
              EdgeDetector.py
              FileImageReader.py
              ImageUtilities.py
              ReferenceImage.py
  DESTINATION ${INSTALL_DIR}/python)
