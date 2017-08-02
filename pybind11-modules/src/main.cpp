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

#include "RemoteData.h"

#define WIN32_LEAN_AND_MEAN
#pragma comment(lib,"ws2_32.lib")

struct RemoteControl {
	int	udp_key;
	RemoteControlComau COMAU;
};

struct RemoteFeedback {
	float t;
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

	char rx_buff[sizeof(RemoteFeedback)];
	char tx_buff[sizeof(RemoteControl)];

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
				WSACleanup();
				exit(EXIT_FAILURE);
			}

			tx_mtx.lock();
			tx_size = sendto(sock, tx_buff, sizeof(tx_buff), 0, (struct sockaddr*) &si_client, slen);
			tx_mtx.unlock();

			if (tx_size == SOCKET_ERROR) {
				std::cout << "sendto() failed with error code: " << WSAGetLastError() << std::endl;
				WSACleanup();
				exit(EXIT_FAILURE);
			}

			
		}
	}

public:
	RemoteFeedback *Feedback;
	RemoteControl *Control;

	UdpServer(unsigned int port) : run_thread() {
		slen = sizeof(si_client);

		Feedback = reinterpret_cast<RemoteFeedback*>(rx_buff);
		Control = reinterpret_cast<RemoteControl*>(tx_buff);

		if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0)
		{
			std::cout << "WSA Startup Failed. Error Code: " <<  WSAGetLastError() << std::endl;
			WSACleanup();
			exit(EXIT_FAILURE);
		}

		if ((sock = (socket(AF_INET, SOCK_DGRAM, 0))) == INVALID_SOCKET)
		{
			std::cout << "Could not create socket: " << WSAGetLastError() << std::endl;
			WSACleanup();
			exit(EXIT_FAILURE);
		}
		std::cout << "Socket created" << std::endl;

		si_server.sin_family = AF_INET;
		si_server.sin_addr.s_addr = INADDR_ANY;
		si_server.sin_port = htons(port);

		if (bind(sock, (struct sockaddr*) &si_server, sizeof(si_server)) == SOCKET_ERROR)
		{
			std::cout << "Bind failed with error code: " << WSAGetLastError() << std::endl;
			WSACleanup();
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

			WSACleanup();
			closesocket(sock);
		}
	}
};

PYBIND11_PLUGIN(udp) {
	// Module
	py::module m("udp", "Udp server and client utilites");

	// Feedback structs
	py::class_<RemoteFeedbackStewart>(m, "RemoteFeedbackStewart")
		.def(py::init<>())
		.def_readonly("x", &RemoteFeedbackStewart::x)
		.def_readonly("y", &RemoteFeedbackStewart::y)
		.def_readonly("z", &RemoteFeedbackStewart::z)
		.def_readonly("roll", &RemoteFeedbackStewart::roll)
		.def_readonly("pitch", &RemoteFeedbackStewart::pitch)
		.def_readonly("yaw", &RemoteFeedbackStewart::yaw)
		.def_readonly("x_t", &RemoteFeedbackStewart::x_t)
		.def_readonly("y_t", &RemoteFeedbackStewart::y_t)
		.def_readonly("z_t", &RemoteFeedbackStewart::z_t)
		.def_readonly("roll_t", &RemoteFeedbackStewart::roll_t)
		.def_readonly("pitch_t", &RemoteFeedbackStewart::pitch_t)
		.def_readonly("yaw_t", &RemoteFeedbackStewart::yaw_t)
		.def_readonly("x_tt", &RemoteFeedbackStewart::x_tt)
		.def_readonly("y_tt", &RemoteFeedbackStewart::y_tt)
		.def_readonly("z_tt", &RemoteFeedbackStewart::z_tt)
		.def_readonly("roll_tt", &RemoteFeedbackStewart::roll_tt)
		.def_readonly("pitch_tt", &RemoteFeedbackStewart::pitch_tt)
		.def_readonly("yaw_tt", &RemoteFeedbackStewart::yaw_tt)
		.def_readonly("L1", &RemoteFeedbackStewart::L1)
		.def_readonly("L2", &RemoteFeedbackStewart::L2)
		.def_readonly("L3", &RemoteFeedbackStewart::L3)
		.def_readonly("L4", &RemoteFeedbackStewart::L4)
		.def_readonly("L5", &RemoteFeedbackStewart::L5)
		.def_readonly("L6", &RemoteFeedbackStewart::L6);

	py::class_<RemoteFeedbackComau>(m, "RemoteFeedbackComau")
		.def(py::init<>())
		.def_readonly("q1", &RemoteFeedbackComau::q1)
		.def_readonly("q2", &RemoteFeedbackComau::q2)
		.def_readonly("q3", &RemoteFeedbackComau::q3)
		.def_readonly("q4", &RemoteFeedbackComau::q4)
		.def_readonly("q5", &RemoteFeedbackComau::q5)
		.def_readonly("q6", &RemoteFeedbackComau::q6)
		.def_readonly("q1_t", &RemoteFeedbackComau::q1_t)
		.def_readonly("q2_t", &RemoteFeedbackComau::q2_t)
		.def_readonly("q3_t", &RemoteFeedbackComau::q3_t)
		.def_readonly("q4_t", &RemoteFeedbackComau::q4_t)
		.def_readonly("q5_t", &RemoteFeedbackComau::q5_t)
		.def_readonly("q6_t", &RemoteFeedbackComau::q6_t)
		.def_readonly("q1_tt", &RemoteFeedbackComau::q1_tt)
		.def_readonly("q2_tt", &RemoteFeedbackComau::q2_tt)
		.def_readonly("q3_tt", &RemoteFeedbackComau::q3_tt)
		.def_readonly("q4_tt", &RemoteFeedbackComau::q4_tt)
		.def_readonly("q5_tt", &RemoteFeedbackComau::q5_tt)
		.def_readonly("q6_tt", &RemoteFeedbackComau::q6_tt);

	py::class_<RemoteFeedbackLeica>(m, "RemoteFeedbackLeica")
		.def(py::init<>())
		.def_readonly("x", &RemoteFeedbackLeica::x)
		.def_readonly("y", &RemoteFeedbackLeica::y)
		.def_readonly("z", &RemoteFeedbackLeica::z)
		.def_readonly("q0", &RemoteFeedbackLeica::q0)
		.def_readonly("q1", &RemoteFeedbackLeica::q1)
		.def_readonly("q2", &RemoteFeedbackLeica::q2)
		.def_readonly("q3", &RemoteFeedbackLeica::q3);

	py::class_<RemoteFeedback>(m, "RemoteFeedback")
		.def(py::init<>())
		.def_readonly("t", &RemoteFeedback::t)
		.def_readonly("EM1500", &RemoteFeedback::EM1500)
		.def_readonly("EM8000", &RemoteFeedback::EM8000)
		.def_readonly("COMAU", &RemoteFeedback::COMAU)
		.def_readonly("AT960", &RemoteFeedback::AT960);

	// Control structs
	py::class_<RemoteControlComau>(m, "RemoteControlComau")
		.def(py::init<>())
		.def_readwrite("q1", &RemoteControlComau::q1)
		.def_readwrite("q2", &RemoteControlComau::q2)
		.def_readwrite("q3", &RemoteControlComau::q3)
		.def_readwrite("q4", &RemoteControlComau::q4)
		.def_readwrite("q5", &RemoteControlComau::q5)
		.def_readwrite("q6", &RemoteControlComau::q6)
		.def_readwrite("q1_t", &RemoteControlComau::q1_t)
		.def_readwrite("q2_t", &RemoteControlComau::q2_t)
		.def_readwrite("q3_t", &RemoteControlComau::q3_t)
		.def_readwrite("q4_t", &RemoteControlComau::q4_t)
		.def_readwrite("q5_t", &RemoteControlComau::q5_t)
		.def_readwrite("q6_t", &RemoteControlComau::q6_t)
		.def_readwrite("q1_tt", &RemoteControlComau::q1_tt)
		.def_readwrite("q2_tt", &RemoteControlComau::q2_tt)
		.def_readwrite("q3_tt", &RemoteControlComau::q3_tt)
		.def_readwrite("q4_tt", &RemoteControlComau::q4_tt)
		.def_readwrite("q5_tt", &RemoteControlComau::q5_tt)
		.def_readwrite("q6_tt", &RemoteControlComau::q6_tt);

	py::class_<RemoteControl>(m, "RemoteControl")
		.def(py::init<>())
		.def_readwrite("udp_key", &RemoteControl::udp_key)
		.def_readwrite("COMAU", &RemoteControl::COMAU);


	// Udp server class define
	py::class_<UdpServer>(m, "server")
		.def(py::init<unsigned int>())
		.def("start", &UdpServer::start)
		.def("close", &UdpServer::close)
		.def_readonly("Feedback", &UdpServer::Feedback)
		.def_readwrite("Control", &UdpServer::Control);

	// Return module
	return m.ptr();
}


int main(int argc, char** argv)
{
	UdpServer udp(50060);
	

	return 0;
}
