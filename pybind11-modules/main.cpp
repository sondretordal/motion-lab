//#include <pybind11/pybind11.h>
//#include <pybind11/numpy.h>
//#include <pybind11/stl.h>

#include "udpserver.hpp"


#include <iostream>
// Test program to use udp server class
int main()
{
  UdpServer udp;

  udp.start();


  udp.stop();

  return 0;
}
