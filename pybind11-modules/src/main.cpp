#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>


#include <iostream>

#include "udpserver.hpp"

int main(int argc, char** argv)
{

  UdpServer udp;
  udp.Start();
  int a = 0;
  while (a < 10) {
    std::cout << "a = " << a << std::endl;
    std::this_thread::sleep_for(std::chrono::milliseconds(500));
    a++;
  }
  udp.Stop();

  /*
  MyClass test;
  test.start();
  std::this_thread::sleep_for (std::chrono::seconds(5));
  test.stop();
  */


  return 0;
}
