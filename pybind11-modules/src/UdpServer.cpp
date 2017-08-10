#include "UdpServer.h"

UdpServer::UdpServer(unsigned int port, void *rx_data, unsigned int rx_size, void *tx_data, unsigned int tx_size) :
    rx_data(rx_data), rx_size(rx_size), tx_data(tx_data), tx_size(tx_size) {

    server.sin_family = AF_INET;
    server.sin_addr.s_addr = INADDR_ANY;
    server.sin_port = htons(port);
    
    if (max(rx_size, tx_size) > MAX_BUFFER_SIZE) {
        std::cout << "Error: Max send/receive buffer is " << MAX_BUFFER_SIZE << " bytes" << std::endl;
        exit(EXIT_FAILURE);
    }

    if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0)
    {
        std::cout << "WSA Startup Failed. Error Code: " <<  WSAGetLastError() << std::endl;
        WSACleanup();
        exit(EXIT_FAILURE);
    }

    if ((sock = (socket(AF_INET, SOCK_DGRAM, 0))) == INVALID_SOCKET)
    {
        std::cout << "Could not create socket: " << WSAGetLastError() << std::endl;
        WSACleanup();
        exit(EXIT_FAILURE);
    }
    std::cout << "Socket created" << std::endl;

    if (bind(sock, (struct sockaddr*) &server, sizeof(server)) == SOCKET_ERROR)
    {
        std::cout << "Bind failed with error code: " << WSAGetLastError() << std::endl;
        WSACleanup();
        exit(EXIT_FAILURE);
    }
    std::cout << "Socket bind done" << std::endl;
}

UdpServer::~UdpServer() {
    WSACleanup();
    closesocket(sock);
}

void UdpServer::check_received() {
    if (recvfrom(sock, rx_buff, rx_size, 0, (struct sockaddr*) &client, &slen) == SOCKET_ERROR) {
        std::cout << "recvfrom() failed with error code: " << WSAGetLastError() << std::endl;
        WSACleanup();
        exit(EXIT_FAILURE);
    }
    memcpy(rx_data, &rx_buff, rx_size);
    memcpy(&tx_buff, tx_data, tx_size);
    
    if (sendto(sock, tx_buff, tx_size, 0, (struct sockaddr*) &client, slen) == SOCKET_ERROR) {
        std::cout << "sendto() failed with error code: " << WSAGetLastError() << std::endl;
        WSACleanup();
        exit(EXIT_FAILURE);
    }
}
