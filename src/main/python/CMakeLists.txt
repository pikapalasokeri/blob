cmake_minimum_required (VERSION 3.5)
project (blob_src_main_python)

set(PROJECT_SOURCE_DIR .)

install(FILES Classifier.py
              ClassifierPipelineCreator.py
              CoherentPointDriftMatcher.py
              ConfigCreator.py
              DirectoryImageReader.py
              EdgeDetectionConfig.py
              EdgeDetector.py
              FileImageReader.py
              GpioPinHandler.py
              ImageGrabber.py
              ImageGrid.py
              ImageProcessingPipeline.py
              ImageTableModel.py
              ImageUtilities.py
              JsonPipelineParser.py
              PipelineStage.py
              PointCloud.py
              PointCloudCreator.py
              PointCloudHandler.py
              PointUtilities.py
              QImageUtilities.py
              ReferenceImage.py
              ResultHandler.py
              TopologyEditorWidget.py
  DESTINATION ${INSTALL_DIR}/python)
