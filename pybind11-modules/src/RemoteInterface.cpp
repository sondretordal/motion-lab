#include "RemoteInterface.h"


RemoteInterface::RemoteInterface(unsigned int port) :
thread(), logger(), server(port, &rx_data, sizeof(rx_data), &tx_data, sizeof(tx_data)) {

    // for (int i = 0; i < 6; i++) {
    //     test.push_back(static_cast<float>(i));
    // }

    float arr [3];

    arr[0] = -42.0f;
    arr[1] = 13.0f;
    arr[2] = 7.2f;

    memcpy(&test, &arr, sizeof(test));

    std::cout << sizeof(test) << std::endl;
}

RemoteInterface::~RemoteInterface() {
    close();
    clear_log();
}

void RemoteInterface::log() {
    log_mode = 1;
}

void RemoteInterface::async_log() {
    log_mode = 2;
}

void RemoteInterface::clear_log() {
    log_mode = 0;
    logger.clear();
}

void RemoteInterface::save_log(std::string path) {
    log_mode = 0;
    logger.save(path);
}

void RemoteInterface::start() {
    running = true;
    thread = std::thread(&RemoteInterface::run, this);
}

void RemoteInterface::close() {
    running = false;
    if (thread.joinable()) {
        thread.join();
        std::cout << "Thread joined sucessfully!" << std::endl;
    }
}
    
void RemoteInterface::update() {
    // Update public feedback and control data
    feedback = rx_data;
    tx_data = control;

    if (log_mode == 1) {
        // Append new data to JSON log
        logger.feedback.push_back(rx_data);
        logger.control.push_back(tx_data);
    }
    
}

void RemoteInterface::run() {
    while (running) {
        // Check for new recieved data
        mutex.lock();
        server.check_received();
        mutex.unlock();

        if ((log_mode == 2)) {
            // Append new data to JSON log
            logger.feedback.push_back(rx_data);
            logger.control.push_back(tx_data);
        }
            
    }
}