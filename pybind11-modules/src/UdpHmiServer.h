#pragma once
#include <pybind11/pybind11.h>

#include <iostream>
#include <vector>
#include <algorithm>
#include <thread>
#include <mutex>
#include <winsock2.h>

#include "DataStructures.h"
#include "DataLogger.h"

#define WIN32_LEAN_AND_MEAN
#pragma comment(lib,"ws2_32.lib")

// Threads in classes: https://rafalcieslak.wordpress.com/2014/05/16/c11-stdthreads-managed-by-a-designated-class/
class UdpHmiServer
{
private:
	SOCKET sock;
	WSADATA wsa;
	int slen;
	struct sockaddr_in si_server, si_client;

	char rx_buff[sizeof(HmiFeedback)];
	char tx_buff[sizeof(HmiControl)];

	HmiFeedback *rx_data;
	HmiControl *tx_data;

	int rx_size;
	int tx_size;

	LogData log_data;

	unsigned int log_count = 0;

	bool logging = false;
	bool running = false;

	std::thread run_thread;
	std::mutex mtx;

	void run();

public:
    // HMI ata which is accessible from Python
	RemoteControl Control;
	RemoteFeedback Feedback;
	unsigned int counter = 0;
	
    UdpHmiServer(unsigned int port);
	~UdpHmiServer();

	void start();
	void close();

	void start_log() {
		logging = true;
		std::cout << "Logging started" << std::endl;
	};

	void clear_log() {
		logging = false;

		std::cout << log_data.Control.size() << std::endl;
		std::cout << log_data.Feedback.size() << std::endl;

		log_data.Control.clear();
		log_data.Feedback.clear();


		std::cout << "Log have been cleared!" << std::endl;
		std::cout << log_data.Control.size() << std::endl;
		std::cout << log_data.Feedback.size() << std::endl;
	};

	void save_log(std::string path) {
		logging = false;
		DataLogger logger(path);
		logger.save(log_data);
		logger.close();

		std::cout << "JSON log saved to: " << path << std::endl;
	};

};