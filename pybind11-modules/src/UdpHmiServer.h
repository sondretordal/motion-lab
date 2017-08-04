#pragma once

#include <iostream>
#include <thread>
#include <mutex>
#include <winsock2.h>

#include "RemoteData.h"

#define WIN32_LEAN_AND_MEAN
#pragma comment(lib,"ws2_32.lib")

struct HmiFeedback {
	RemoteControl Control;
	RemoteFeedback Feedback;
};

struct HmiControl {
	unsigned int counter;
};

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
};