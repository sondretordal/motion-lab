#ifndef __URSERVER_HPP__
#define __URSERVER_HPP__

#include <iostream>
#include <string>
#include <thread>
#include <mutex>

#include <stdio.h>

#include <winsock2.h>
#define WIN32_LEAN_AND_MEAN
#pragma comment(lib,"ws2_32.lib") //Winsock Library

struct tx_data
{
  float data[50];
};

struct rx_data
{
  float data[50];
};

class UdpServer
{
private:
  int s, slen;
  WSADATA wsa;
  struct sockaddr_in server, client;

  char tx_buff[sizeof(tx_data)];
  char rx_buff[sizeof(rx_data)];

  tx_data *tx;
  rx_data *rx;

public:
  UdpServer(unsigned int port = 50050) {

    slen  = sizeof(client);

    tx = reinterpret_cast<tx_data*>(tx_buff);
    rx = reinterpret_cast<rx_data*>(rx_buff);

  	if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0)
  	{
  		std::cout << "WSA Startup Failed. Error Code: " <<  WSAGetLastError() << std::endl;
  		exit(EXIT_FAILURE);
  	}

  	if ((s = static_cast<int>(socket(AF_INET, SOCK_DGRAM, 0))) == INVALID_SOCKET)
  	{
  		printf("Could not create socket : %d", WSAGetLastError());
      exit(EXIT_FAILURE);
  	}
  	printf("Socket created.\n");

  	server.sin_family = AF_INET;
  	server.sin_addr.s_addr = INADDR_ANY;
  	server.sin_port = htons(port);

  	if (bind(s, (struct sockaddr*) &server, sizeof(server)) == SOCKET_ERROR)
  	{
  		printf("Bind failed with error code : %d", WSAGetLastError());
  		exit(EXIT_FAILURE);
  	}
  	puts("Bind done");
    int count = 0;
    while (true)
    {

      if (recvfrom(s, rx_buff, sizeof(rx_buff), 0, (struct sockaddr*) &client, &slen) == SOCKET_ERROR) {
        printf("recvfrom() failed with error code : %d", WSAGetLastError());
        exit(EXIT_FAILURE);
      }

      std::cout << "rx.data[0] " << rx->data[0] << std::endl;

      for (int i = 0; i < 50; i++) {
        tx->data[i] = count;

      }
      count++;

      if (sendto(s, tx_buff, sizeof(tx_buff), 0, (struct sockaddr*) &client, slen) == SOCKET_ERROR) {
        printf("sendto() failed with error code : %d" , WSAGetLastError());
        exit(EXIT_FAILURE);
      }

    }

  }

  void start() {

  }

  void stop() {

  }



};





#endif
