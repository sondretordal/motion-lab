#include "RemoteInterface.h"


RemoteInterface::RemoteInterface(unsigned int port) :
thread(), logger(), server(port, &rx_data, sizeof(rx_data), &tx_data, sizeof(tx_data)) {

}

RemoteInterface::~RemoteInterface() {
    close();
    clear_log();
}

void RemoteInterface::start_log() {
    update_data = true;
}
void RemoteInterface::clear_log() {
    update_data = false;
    logger.clear();
}
void RemoteInterface::save_log(std::string path) {
    update_data = false;
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
    update_data = true;
}

void RemoteInterface::run() {
    while (running) {
        mutex.lock();
        server.check_received();
        mutex.unlock();

        if (update_data) {
            // Update public feedback and control data
            feedback = rx_data;
            tx_data = control;
        
            // Append new data to JSON log
            logger.feedback.push_back(feedback);
            logger.control.push_back(control);
            
            update_data = false;

        }
        
    }
}