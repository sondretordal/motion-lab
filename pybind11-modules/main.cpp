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

#include "inc/datastructures.hpp"

#define WIN32_LEAN_AND_MEAN
#pragma comment(lib,"ws2_32.lib")


struct RemoteControl {
	int	udp_key;
	RemoteControlComau COMAU;
};

struct RemoteFeedback {
	RemoteFeedbackStewart EM1500;
	RemoteFeedbackStewart EM8000;
	RemoteFeedbackComau COMAU;
	RemoteFeedbackLeica AT960;
};

namespace py = pybind11;

// Threads in classes: https://rafalcieslak.wordpress.com/2014/05/16/c11-stdthreads-managed-by-a-designated-class/
class UdpServer
{
private:
	SOCKET sock;
	WSADATA wsa;
	int slen;
	struct sockaddr_in si_server, si_client;

	char rx_buff[296];
	char tx_buff[4];

	int rx_size;
	int tx_size;

	bool running = false;

	std::thread run_thread;
	std::mutex tx_mtx, rx_mtx;

	void run() {
		while (running) {
			rx_mtx.lock();
			rx_size = recvfrom(sock, rx_buff, sizeof(rx_buff), 0, (struct sockaddr*) &si_client, &slen);
			rx_mtx.unlock();

			if (rx_size == SOCKET_ERROR) {
				std::cout << "recvfrom() failed with error code: " << WSAGetLastError() << std::endl;
				exit(EXIT_FAILURE);
			}

			tx_mtx.lock();
			tx_size = sendto(sock, tx_buff, sizeof(tx_buff), 0, (struct sockaddr*) &si_client, slen);
			tx_mtx.unlock();

			if (tx_size == SOCKET_ERROR) {
				std::cout << "sendto() failed with error code: " << WSAGetLastError() << std::endl;
				exit(EXIT_FAILURE);
			}
		}
	}

public:
	UdpServer(unsigned int port) : run_thread() {
		slen = sizeof(si_client);

		if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0)
		{
			std::cout << "WSA Startup Failed. Error Code: " <<  WSAGetLastError() << std::endl;
			exit(EXIT_FAILURE);
		}

		if ((sock = (socket(AF_INET, SOCK_DGRAM, 0))) == INVALID_SOCKET)
		{
			std::cout << "Could not create socket: " << WSAGetLastError() << std::endl;
			exit(EXIT_FAILURE);
		}
		std::cout << "Socket created" << std::endl;

		si_server.sin_family = AF_INET;
		si_server.sin_addr.s_addr = INADDR_ANY;
		si_server.sin_port = htons(port);

		if (bind(sock, (struct sockaddr*) &si_server, sizeof(si_server)) == SOCKET_ERROR)
		{
			std::cout << "Bind failed with error code: " << WSAGetLastError() << std::endl;
			exit(EXIT_FAILURE);
		}
		std::cout << "Socket bind done" << std::endl;
	}
	~UdpServer() {
		close();
	}

	void start() {
		running = true;
		run_thread = std::thread(&UdpServer::run, this);
	}

	void close() {
		running = false;
		if (run_thread.joinable()) {
			run_thread.join();
			std::cout << "UDP thread joined sucessfully!" << std::endl;

			closesocket(sock);
			WSACleanup();
		}
	}

	void send(char* bytes) {
		tx_mtx.lock();
		memcpy(&tx_buff, bytes, sizeof(tx_buff));
		tx_mtx.unlock();
	}

	py::bytes recv() {
		rx_mtx.lock();
		std::string str( rx_buff, rx_buff + sizeof rx_buff / sizeof rx_buff[0]);
		rx_mtx.unlock();

		return py::bytes(str);
	}


	A test1(A in) {
		A out;

		out.x = 2*in.x;
		out.y = 2*in.y;
		out.z = 2*in.z;
		
		return out;
	}
	
	B test2(B in) {
		B out;

		out.s1 = in.s2;
		out.s2 = in.s1;

		return out;
	}

};



PYBIND11_PLUGIN(udp) {
	// Module
	py::module m("udp", "Udp server and client utilites");

	py::class_<A> A(m, "A");
	A.def(py::init<>());
	A.def_readwrite("x", &A::x);
	A.def_readwrite("y", &A::y);
	A.def_readwrite("z", &A::z);

	py::class_<B> B(m, "B");
	B.def(py::init<>());
	B.def_readwrite("s1", &B::s1);
	B.def_readwrite("s2", &B::s2);

	
	// Udp server
	py::class_<UdpServer> server(m, "server");
	server.def(py::init<unsigned int>());
	server.def("start", &UdpServer::start);
	server.def("close", &UdpServer::close);
	server.def("send", &UdpServer::send);
	server.def("recv", &UdpServer::recv);

	// server.def("test1", &UdpServer::Test1, py::arg("arg") = A());
	server.def("test1", &UdpServer::test1);
	server.def("test2", &UdpServer::test2);

	return m.ptr();
}


int main(int argc, char** argv)
{
  // UdpServer udp;
  // udp.start();


  // int a = 0;
  // while (a < 10) {
  //   std::cout << "a = " << a << std::endl;
  //   std::this_thread::sleep_for(std::chrono::milliseconds(500));
  //   a++;
  // }
  // udp.close();

  return 0;
}
