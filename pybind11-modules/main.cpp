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

struct RxStruct {
	unsigned int udpKey;
};

struct TxStruct {
	float t;
	float EM1500_x;
	float EM1500_y;
	float EM1500_z;
	float EM1500_roll;
	float EM1500_pitch;
	float EM1500_yaw;
	float EM1500_x_t;
	float EM1500_y_t;
	float EM1500_z_t;
	float EM1500_roll_t;
	float EM1500_pitch_t;
	float EM1500_yaw_t;
	float EM1500_x_tt;
	float EM1500_y_tt;
	float EM1500_z_tt;
	float EM1500_roll_tt;
	float EM1500_pitch_tt;
	float EM1500_yaw_tt;
	float EM1500_L1;
	float EM1500_L2;
	float EM1500_L3;
	float EM1500_L4;
	float EM1500_L5;
	float EM1500_L6;
	float EM8000_x;
	float EM8000_y;
	float EM8000_z;
	float EM8000_roll;
	float EM8000_pitch;
	float EM8000_yaw;
	float EM8000_x_t;
	float EM8000_y_t;
	float EM8000_z_t;
	float EM8000_roll_t;
	float EM8000_pitch_t;
	float EM8000_yaw_t;
	float EM8000_x_tt;
	float EM8000_y_tt;
	float EM8000_z_tt;
	float EM8000_roll_tt;
	float EM8000_pitch_tt;
	float EM8000_yaw_tt;
	float EM8000_L1;
	float EM8000_L2;
	float EM8000_L3;
	float EM8000_L4;
	float EM8000_L5;
	float EM8000_L6;
	float q1;
	float q2;
	float q3;
	float q4;
	float q5;
	float q6;
	float q1_t;
	float q2_t;
	float q3_t;
	float q4_t;
	float q5_t;
	float q6_t;
	float q1_tt;
	float q2_tt;
	float q3_tt;
	float q4_tt;
	float q5_tt;
	float q6_tt;
	float AT960_x;
	float AT960_y;
	float AT960_z;
	float AT960_q0;
	float AT960_q1;
	float AT960_q2;
	float AT960_q3;
};

struct Data {
	RxStruct rx;
	TxStruct tx;
};

namespace py = pybind11;

// Threads in classes: https://rafalcieslak.wordpress.com/2014/05/16/c11-stdthreads-managed-by-a-designated-class/
class UdpServer
{
private:
	int s, slen;
	WSADATA wsa;
	struct sockaddr_in si_server, si_client;

	char rx_buff[500];
	//char tx_buff[sizeof(TxData)];

	bool running = false;

	std::thread run_thread;
	std::mutex mtx;

	

	void Run() {
		while (running) {
			if (recvfrom(s, rx_buff, sizeof(rx_buff), 0, (struct sockaddr*) &si_client, &slen) == SOCKET_ERROR) {
				std::cout << "recvfrom() failed with error code: " << WSAGetLastError() << std::endl;
				exit(EXIT_FAILURE);
			}

			// if (sendto(s, tx_buff, sizeof(tx_buff), 0, (struct sockaddr*) &si_client, slen) == SOCKET_ERROR) {
			// 	std::cout << "sendto() failed with error code: " << WSAGetLastError() << std::endl;
			// 	exit(EXIT_FAILURE);
			// }
		}
	}

public:

	UdpServer(unsigned int port, unsigned int rx_size, unsigned int tx_size) : run_thread() {
		slen = sizeof(si_client);

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

	// void Send(char* bytes) {
	// 	mtx.lock();
	// 	memcpy(&tx_buff, bytes, sizeof(tx_buff));
	// 	mtx.unlock();
	// }

	// py::bytes Recv() {
	// 	mtx.lock();
	// 	std::string str( rx_buff, rx_buff + sizeof rx_buff / sizeof rx_buff[0]);
	// 	mtx.unlock();
	// 	return py::bytes(str);
	// }

	
};


PYBIND11_PLUGIN(udp) {
	// Module
	py::module m("udp", "Udp server and client utilites");
	// Constructor
	py::class_<UdpServer> server(m, "server");
	server.def(py::init<unsigned int, unsigned int, unsigned int>());
	server.def("start", &UdpServer::Start);
	server.def("close", &UdpServer::Close);
	// server.def("send", &UdpServer::Send);
	// server.def("recv", &UdpServer::Recv);


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
