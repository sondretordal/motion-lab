#include "RemoteInterface.h"


RemoteInterface::RemoteInterface(unsigned int port) :
thread(), logger(), server(port, &rx_data, sizeof(rx_data), &tx_data, sizeof(tx_data)) {

}

RemoteInterface::~RemoteInterface() {
    close();
    clear_log();
}

void RemoteInterface::log() {
    log_mode = 1;
}

void RemoteInterface::async_log(unsigned int cycletime) {
    log_mode = 2;
    cycletime = cycletime;
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

        // Increment cycletime counter
        counter++;

        if ((log_mode == 2) && (counter >= 100)) {
            // Append new data to JSON log
            logger.feedback.push_back(rx_data);
            logger.control.push_back(tx_data);

            // Reset counter
            counter = 0;
        }
            
    }
}