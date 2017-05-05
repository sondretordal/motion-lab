#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/stl.h>

#include <iostream>

#include "udpserver.hpp"

namespace py = pybind11;



PYBIND11_PLUGIN(MotionLab) {
    py::module m("MotionLab", "Motion-Laboratory Python Interface");
    py::class_<UdpServer> udp(m, "udpserver");
    udp.def(py::init<const unsigned int &>());
    udp.def("start", &UdpServer::Start);
    udp.def("close", &UdpServer::Close);
    udp.def("recv_data", &UdpServer::RecvData);
    udp.def("send_data", &UdpServer::SendData);
    udp.def_readwrite("test", &UdpServer::test);
    
    return m.ptr();
}

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
  udp.Close();

  return 0;
}
