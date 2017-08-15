#pragma once

#include "UdpServer.h"
#include "JsonLogger.h"
#include "DataStructures.h"

struct RxData {
    RemoteControl control;
    RemoteFeedback feedback;
};

struct TxData {
    unsigned int counter = 0;
};

class HmiInterface
{
private:
    // Threaded UdpServer class
    UdpServer server;

    // Thread related
	std::thread thread;
	std::mutex mutex;
    bool running = false;
    void run();

    // Logging feature
    JsonLogger logger;
    bool logging = false;
    unsigned int ms_counter = 0;
    unsigned int ms_rate = 1;

    // Hmi data
    RxData rx_data;
	TxData tx_data;
    
public:
    // control and feedback data
    RemoteFeedback feedback;
    RemoteControl control;

    // Constructor and destructor
    HmiInterface(unsigned int port);
    ~HmiInterface();

    // Member functions
    void start();
    void close();
    void update();

    void start_log(std::string update_rate);
    void clear_log();
    void save_log(std::string path);
};