#pragma once

#include <iostream>
#include <thread>
#include <mutex>
#include <winsock2.h>

#include "DataStructures.h"

#define WIN32_LEAN_AND_MEAN
#pragma comment(lib,"ws2_32.lib")

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
	std::mutex mtx;

	void run();

public:
    // IO data which is accessible from Python
	RemoteFeedback *Feedback;
	RemoteControl *Control;

    UdpServer(unsigned int port);
	~UdpServer();

	void start();
	void close();
};