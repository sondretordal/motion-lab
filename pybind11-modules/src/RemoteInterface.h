#pragma once

#include "UdpServer.h"
#include "DataStructures.h"

class RemoteInterface
{
private:
    // Threaded UdpServer class
    UdpServer server;

public:
    RemoteFeedback Feedback;
	RemoteControl Control;

    RemoteInterface(unsigned int port) :
    server(50060, &Feedback, sizeof(Feedback), &Control, sizeof(Control)) {

    }
    
    ~RemoteInterface() {

    };



    void start() {

    };


    void close() {

    };

};