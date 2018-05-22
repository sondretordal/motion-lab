# Include directories
include_directories(
  SYSTEM
  ${CONAN_INCLUDE_DIRS}
  ${PYTHON_INCLUDE_DIRS}
  C:/TwinCAT/AdsApi/TcAdsDll/Include
)

# Main Executable
add_executable(main
  main.cpp
)

target_link_libraries(main
  ${PYTHON_LIBRARIES}
  C:/TwinCAT/AdsApi/TcAdsDll/x64/lib/TcAdsDll.lib
)

# Shared pybind11 module settings
add_library(${CMAKE_PROJECT_NAME} SHARED
  main.cpp
  JsonLogger.cpp
)

# Rename module file ending from .dll to .pyd
set_target_properties(${CMAKE_PROJECT_NAME} PROPERTIES SUFFIX ".pyd")

target_link_libraries(${CMAKE_PROJECT_NAME}
  ${PYTHON_LIBRARIES}
  C:/TwinCAT/AdsApi/TcAdsDll/x64/lib/TcAdsDll.lib
)



