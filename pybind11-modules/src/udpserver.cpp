#include "udpserver.hpp"

UdpServer::UdpServer(unsigned int port) : run_thread() {
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

UdpServer::~UdpServer() {
    Stop();
  }

void UdpServer::Start() {
  run_thread = std::thread(&UdpServer::Run, this);
}

void UdpServer::Stop() {
  running = false;
  if (run_thread.joinable()) {
     run_thread.join();
     std::cout << "UDP thread joined sucessfully!" << std::endl;
  }
}

void UdpServer::Run() {
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
