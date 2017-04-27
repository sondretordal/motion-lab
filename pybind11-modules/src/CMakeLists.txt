
include_directories (
  SYSTEM
  ${CONAN_INCLUDE_DIRS}
  ${PYTHON_INCLUDE_DIRS}
  ${PybindModules_SOURCE_DIR}/inc
)

add_executable (
  ${CMAKE_PROJECT_NAME}
  main.cpp
  udpserver.cpp
)

target_link_libraries (
  ${CMAKE_PROJECT_NAME}
  ${PYTHON_LIBRARIES}
)
