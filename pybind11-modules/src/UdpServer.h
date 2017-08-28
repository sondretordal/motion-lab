#pragma once

#include <iostream>
#include <winsock2.h>

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
	struct sockaddr_in server, client;
	int slen = sizeof(client);

	// Receive and send buffers and data pointers
	char rx_buff[MAX_BUFFER_SIZE];
	char tx_buff[MAX_BUFFER_SIZE];

	unsigned int rx_size;
	unsigned int tx_size;

	void *rx_data;
	void *tx_data;
public:
	

	// Constructor and destructor
    UdpServer(unsigned int port, void *rx_data, unsigned int rx_size, void *tx_data, unsigned int tx_size);
	~UdpServer();

	// Check received
	void check_received();
};