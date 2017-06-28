#ifndef __URSERVER_HPP__
#define __URSERVER_HPP__

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

// Threads in classes: https://rafalcieslak.wordpress.com/2014/05/16/c11-stdthreads-managed-by-a-designated-class/

struct TxData {
  float data[256];
};

struct RxData {
  float data[109];
};

//TxData sst;

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

  std::thread run_thread;
  std::mutex run_mtx;

  void Run();

public:
  UdpServer(unsigned int port = 50050);
  ~UdpServer();

  void Start();
  void Close();
  std::vector<float> RecvData();
  void SendData(float data, int i);
};

#endif
