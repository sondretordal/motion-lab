project(PybindModules)
cmake_minimum_required(VERSION 3.1)

find_package(PythonLibs REQUIRED)
find_package(Threads REQUIRED)

# Conan include and setup
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_subdirectory(src)
