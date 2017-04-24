cmake_minimum_required (VERSION 2.8)


set(CMAKE_CXX_FLAGS "-std=c++11")


set(pybind11_DIR "C:/pybind11/build/mock_install/share/cmake/pybind11")
find_package(pybind11 REQUIRED)


project (main)
add_executable(main
  main.cpp
  udpserver.hpp
)
