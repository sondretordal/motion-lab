#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/numpy.h>

#include <iostream>
#include <vector>
#include <chrono>
#include <string>
#include <thread>
#include <mutex>
#include <stdio.h>
#include <winsock2.h>

#define WIN32_LEAN_AND_MEAN
#pragma comment(lib,"ws2_32.lib")


struct A {
    float x;
    float y;
	float z;
};

namespace py = pybind11;

// Threads in classes: https://rafalcieslak.wordpress.com/2014/05/16/c11-stdthreads-managed-by-a-designated-class/
class UdpServer
{
private:
	int s, slen;
	WSADATA wsa;
	struct sockaddr_in si_server, si_client;

	const unsigned int rx_size;
	const unsigned int tx_size;

	char rx_buff[296];
	char tx_buff[4];

	bool running = false;

	std::thread run_thread;
	std::mutex mtx;

	

	void Run() {
		while (running) {
			if (recvfrom(s, rx_buff, sizeof(rx_buff), 0, (struct sockaddr*) &si_client, &slen) == SOCKET_ERROR) {
				std::cout << "recvfrom() failed with error code: " << WSAGetLastError() << std::endl;
				exit(EXIT_FAILURE);
			}

			//std::cout << "rx_data.data[0] " << rx_data->data[0] << std::endl;
			if (sendto(s, tx_buff, sizeof(tx_buff), 0, (struct sockaddr*) &si_client, slen) == SOCKET_ERROR) {
				std::cout << "sendto() failed with error code: " << WSAGetLastError() << std::endl;
				exit(EXIT_FAILURE);
			}
		}
	}

public:

	UdpServer(unsigned int port, unsigned int rx_size, unsigned int tx_size) : 
		run_thread(), rx_size(rx_size), tx_size(tx_size) {
		slen = sizeof(si_client);

		std::cout << "rx_size = " << rx_size << " sizeof(rx_buff) = " << sizeof(rx_buff) << std::endl;
		std::cout << "tx_size = " << tx_size << " sizeof(tx_buff) = " << sizeof(tx_buff) << std::endl;
		
		if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0)
		{
			std::cout << "WSA Startup Failed. Error Code: " <<  WSAGetLastError() << std::endl;
			exit(EXIT_FAILURE);
		}

		if ((s = static_cast<int>(socket(AF_INET, SOCK_DGRAM, 0))) == INVALID_SOCKET)
		{
			std::cout << "Could not create socket: " << WSAGetLastError() << std::endl;
			exit(EXIT_FAILURE);
		}
		std::cout << "Socket created" << std::endl;

		si_server.sin_family = AF_INET;
		si_server.sin_addr.s_addr = INADDR_ANY;
		si_server.sin_port = htons(port);

		if (bind(s, (struct sockaddr*) &si_server, sizeof(si_server)) == SOCKET_ERROR)
		{
			std::cout << "Bind failed with error code: " << WSAGetLastError() << std::endl;
			exit(EXIT_FAILURE);
		}
		std::cout << "Socket bind done" << std::endl;

		running = true;
	}
	~UdpServer() {
		Close();
	}

	void Start() {
		run_thread = std::thread(&UdpServer::Run, this);
	}

	void Close() {
	running = false;
		if (run_thread.joinable()) {
			run_thread.join();
			std::cout << "UDP thread joined sucessfully!" << std::endl;
		}
	}

	void Send(char* bytes) {
		mtx.lock();
		memcpy(&tx_buff, bytes, sizeof(tx_buff));
		mtx.unlock();
	}

	py::bytes Recv() {
		mtx.lock();
		std::string str( rx_buff, rx_buff + sizeof rx_buff / sizeof rx_buff[0]);
		mtx.unlock();
		return py::bytes(str);
	}

	
	A test(void) {
		A myStruct;

		return myStruct;
	}

	// py::array_t<A> test2(void) {
	// 	return myStruct;
	// }
};


PYBIND11_PLUGIN(udp) {
	PYBIND11_NUMPY_DTYPE(A, x, y, z);
	// Module
	py::module m("udp", "Udp server and client utilites");
	// Constructor
	py::class_<UdpServer> server(m, "server");
	server.def(py::init<unsigned int, unsigned int, unsigned int>());
	server.def("start", &UdpServer::Start);
	server.def("close", &UdpServer::Close);
	server.def("send", &UdpServer::Send);
	server.def("recv", &UdpServer::Recv);

	server.def("test", &UdpServer::test);
	// server.def("test2", &UdpServer::test2);


	return m.ptr();
}


int main(int argc, char** argv)
{
  // UdpServer udp;
  // udp.Start();


  // int a = 0;
  // while (a < 10) {
  //   std::cout << "a = " << a << std::endl;
  //   std::this_thread::sleep_for(std::chrono::milliseconds(500));
  //   a++;
  // }
  // udp.Close();

  return 0;
}
