# Include directories
include_directories(
  SYSTEM
  ${CONAN_INCLUDE_DIRS}
  ${PYTHON_INCLUDE_DIRS}
)

# Executable settings
add_executable(main
  main.cpp
  UdpServer.cpp
  HmiInterface.cpp
  RemoteInterface.cpp
  JsonLogger.cpp
  ShipSimulator.cpp
)

target_link_libraries(main
  ${PYTHON_LIBRARIES}
)

# Shared pybind11 module settings
add_library(${CMAKE_PROJECT_NAME} SHARED
  main.cpp
  UdpServer.cpp
  HmiInterface.cpp
  RemoteInterface.cpp
  JsonLogger.cpp
  ShipSimulator.cpp
)

target_link_libraries(${CMAKE_PROJECT_NAME}
  ${PYTHON_LIBRARIES}
)

# Rename module file ending from .dll to .pyd
set_target_properties(${CMAKE_PROJECT_NAME} PROPERTIES SUFFIX ".pyd")

