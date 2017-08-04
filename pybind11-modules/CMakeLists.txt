project(MotionLab)
cmake_minimum_required(VERSION 3.1)

# Conan include and setup
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)

# Required libs
find_package(PythonLibs REQUIRED)
find_package(Threads REQUIRED)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR})
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_DEBUG ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})

# Add source folder
add_subdirectory(src)

# # Include directories
# include_directories(
#   SYSTEM
#   ${CONAN_INCLUDE_DIRS}
#   ${PYTHON_INCLUDE_DIRS}
# )

# # Executable settings
# add_executable(main
#   main.cpp
# )

# target_link_libraries(main
#   ${PYTHON_LIBRARIES}
# )

# # Shared pybind11 module settings
# add_library(${CMAKE_PROJECT_NAME} SHARED
#   main.cpp
# )

# set_target_properties(${CMAKE_PROJECT_NAME} PROPERTIES SUFFIX ".pyd")

# target_link_libraries(${CMAKE_PROJECT_NAME}
#   ${PYTHON_LIBRARIES}
# )
