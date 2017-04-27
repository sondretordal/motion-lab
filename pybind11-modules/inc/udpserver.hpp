#ifndef __URSERVER_HPP__
#define __URSERVER_HPP__

#include <iostream>
#include <chrono>
#include <string>
#include <thread>
#include <mutex>
#include <stdio.h>


#include <winsock2.h>
#define WIN32_LEAN_AND_MEAN
#pragma comment(lib,"ws2_32.lib")

// Threads in classes: https://rafalcieslak.wordpress.com/2014/05/16/c11-stdthreads-managed-by-a-designated-class/

struct TxData
{
  float data[50];
};

struct RxData
{
  float data[50];
};

class UdpServer
{
private:
  int s, slen;
  WSADATA wsa;
  struct sockaddr_in si_server, si_client;

  char tx_buff[sizeof(TxData)];
  char rx_buff[sizeof(RxData)];

  TxData *tx_data;
  RxData *rx_data;

  bool running = false;
  int count = 0;

  std::thread run_thread;

  void Run() {
    while (running) {
      if (recvfrom(s, rx_buff, sizeof(rx_buff), 0, (struct sockaddr*) &si_client, &slen) == SOCKET_ERROR) {
        std::cout << "recvfrom() failed with error code: " << WSAGetLastError() << std::endl;
        exit(EXIT_FAILURE);
      }

      //std::cout << "rx_data.data[0] " << rx_data->data[0] << std::endl;

      for (int i = 0; i < 50; i++) {
        tx_data->data[i] = static_cast<float>(count);

      }
      count++;

      if (sendto(s, tx_buff, sizeof(tx_buff), 0, (struct sockaddr*) &si_client, slen) == SOCKET_ERROR) {
        std::cout << "sendto() failed with error code: " << WSAGetLastError() << std::endl;
        exit(EXIT_FAILURE);
      }
    }
  }


public:
  UdpServer(unsigned int port = 50050) : run_thread()
  {

    slen = sizeof(si_client);

    tx_data = reinterpret_cast<TxData*>(tx_buff);
    rx_data = reinterpret_cast<RxData*>(rx_buff);

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
  ~UdpServer()
  {
    Stop();
  }

  void Start() {
    run_thread = std::thread(&UdpServer::Run, this);
  }

  void Stop() {
    running = false;
    if (run_thread.joinable()) {
       run_thread.join();
       std::cout << "UDP thread joined sucessfully!" << std::endl;
    }
  }
};

class MyClass{
public:
    MyClass() : the_thread() {}
    ~MyClass()
    {
      stop();
    }
    void start() {
      the_thread = std::thread(&MyClass::ThreadMain, this);
    }
    void stop() {
      stop_thread = true;
      if (the_thread.joinable()) {
         the_thread.join();
         std::cout << "UDP thread joined sucessfully!" << std::endl;
      }
    }

private:
    std::thread the_thread;

    bool stop_thread = false; // Super simple thread stopping.
    void ThreadMain() {
        while(!stop_thread) {
            // Do something useful, e.g:
            std::cout << "hei" << std::endl;

        }
    }

};





#endif
