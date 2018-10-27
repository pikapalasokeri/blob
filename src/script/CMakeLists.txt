cmake_minimum_required (VERSION 3.5)
project (blob_src_script)

set(PROJECT_SOURCE_DIR .)

install(FILES createConfig.py
              DemoBruteForceMatcher.py
              DemoClassifier.py
              DemoEdgeDetector.py
              DemoMatch.py
              DemoSimpleThrow.py
              main.py
              QtConfigCreator.py
              wrapper.sh
  DESTINATION ${INSTALL_DIR}
  PERMISSIONS OWNER_READ OWNER_EXECUTE
              GROUP_READ GROUP_EXECUTE
              WORLD_READ WORLD_EXECUTE)
