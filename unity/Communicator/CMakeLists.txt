cmake_minimum_required(VERSION 2.8.6)
project(animallib)
set (CMAKE_BUILD_TYPE Debug)

#include *.h files under include folder and  
#the project's output folder e.g. Debug
include_directories (include ${PROJECT_BINARY_DIR})

#compile all *.cpp source files under src folder
file (GLOB SOURCES "src/*.cpp")

#output library as animallib.*

#output library export file *.lib and
#output macro definitions include file
include (GenerateExportHeader)
add_library(animallib SHARED ${SOURCES})
GENERATE_EXPORT_HEADER (animallib
    BASE_NAME animallib
    EXPORT_MACRO_NAME animallib_EXPORT
    EXPORT_FILE_NAME animallib_Export.h
    STATIC_DEFINE animallib_BUILT_AS_STATIC
)