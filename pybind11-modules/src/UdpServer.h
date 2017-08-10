#pragma once

#include <iostream>
#include <vector>
#include <thread>
#include <mutex>
#include <winsock2.h>

#include "DataStructures.h"

#define WIN32_LEAN_AND_MEAN
#pragma comment(lib,"ws2_32.lib")

# define MAX_BUFFER_SIZE 1024

// Threads in classes: https://rafalcieslak.wordpress.com/2014/05/16/c11-stdthreads-managed-by-a-designated-class/
class UdpServer
{
private:
	// Winsock vairables
	SOCKET sock;
	WSADATA wsa;
	struct sockaddr_in si_server, si_client;
	int slen = sizeof(si_client);

	// Receive and send buffers and data pointers
	unsigned int rx_size;
	unsigned int tx_size;

	char rx_buff[MAX_BUFFER_SIZE];
	char tx_buff[MAX_BUFFER_SIZE];

	void *rx_data;
	void *tx_data;

	// Thread and mutex lock
	std::thread run_thread;
	std::mutex mtx;

	// Run function to be executeb my thread
	bool running = false;
	void run();
public:
	// Logging
	bool logging = false;

	// Constructor and destructor
    UdpServer(unsigned int port, void *rx_data, unsigned int rx_size, void *tx_data, unsigned int tx_size);
	~UdpServer();

	// Start and stop functionality
	void start();
	void close();
};