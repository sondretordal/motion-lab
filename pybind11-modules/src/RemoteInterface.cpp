#include "RemoteInterface.h"


RemoteInterface::RemoteInterface(unsigned int port) :
thread(), logger(), server(port, sizeof(Feedback), sizeof(Control)) {

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
        server.check_received();

        if (update_data) {
            mutex.lock();
            // Copy data to and from udp buffers
            memcpy(&Feedback, &server.rx_buff, sizeof(Feedback));
            memcpy(&server.tx_buff, &Control, sizeof(Control));
            
            // Append new data to JSON log
            logger.Feedback.push_back(Feedback);
            logger.Control.push_back(Control);
            mutex.unlock();

            update_data = false;
        }
        
    }
}