project(MotionLab)
cmake_minimum_required(VERSION 3.1)

# Conan include and setup
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
#conan_basic_setup()

# Required libs
find_package(PythonLibs REQUIRED)
find_package(Threads REQUIRED)

set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR})
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY_DEBUG ${CMAKE_RUNTIME_OUTPUT_DIRECTORY})


add_subdirectory(src)
