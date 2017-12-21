#pragma once

#include <thread>
#include <mutex>

#include "UdpServer.h"
#include "JsonLogger.h"
#include "DataStructures.h"


class RemoteInterface
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
    unsigned int cycletime = 10;
    unsigned int log_mode = 0;

    // Remote interface data
    Feedback rx_data;
    Control tx_data;
public:

    // IO data
    Feedback feedback;
	Control control;

    // Constructor and destructor
    RemoteInterface(unsigned int port);
    ~RemoteInterface();

    // Member functions
    void start();
    void close();
    void update();

    void log();
    void async_log();
    void clear_log();
    void save_log(std::string path);
};