
include_directories(
  SYSTEM
  ${CONAN_INCLUDE_DIRS}
  ${PYTHON_INCLUDE_DIRS}
  ${MotionLab_SOURCE_DIR}/inc
)
message("CONAN_INCLUDE_DIRS: " ${CONAN_INCLUDE_DIRS})
message("PybindModules_SOURCE_DIR: " ${PybindModules_SOURCE_DIR})

#add_executable (
  #${CMAKE_PROJECT_NAME}
  #main.cpp
  #udpserver.cpp
#)

add_library(${CMAKE_PROJECT_NAME} SHARED
  main.cpp
  udpserver.cpp
)

set_target_properties(${CMAKE_PROJECT_NAME} PROPERTIES SUFFIX ".pyd")

target_link_libraries(${CMAKE_PROJECT_NAME}
  ${PYTHON_LIBRARIES}
)
