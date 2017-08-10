#pragma once

#include "UdpServer.h"
#include "JsonLogger.h"
#include "DataStructures.h"

struct RxData {
    RemoteControl Control;
    RemoteFeedback Feedback;
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
    unsigned int update_freq = 10;
    bool update_data = false;

    // Hmi data
    RxData rx_data;
	TxData tx_data;
    
public:
    // Control and Feedback data
    RemoteFeedback Feedback;
    RemoteControl Control;

    // Constructor and destructor
    HmiInterface(unsigned int port);
    ~HmiInterface();

    // Member functions
    void start();
    void close();
    void update();

    void start_log();
    void clear_log();
    void save_log(std::string path);
};