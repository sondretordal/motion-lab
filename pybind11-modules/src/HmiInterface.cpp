#include "HmiInterface.h"

#include "HmiInterface.h"


HmiInterface::HmiInterface(unsigned int port) :
thread(), logger(), server(port, &rx_data, sizeof(rx_data), &tx_data, sizeof(tx_data)) {

}

HmiInterface::~HmiInterface() {
    close();
    clear_log();
}

void HmiInterface::start_log() {
    update_data = true;
}
void HmiInterface::clear_log() {
    update_data = false;
    logger.clear();
}
void HmiInterface::save_log(std::string path) {
    update_data = false;
    logger.save(path);
}

void HmiInterface::start() {
    running = true;
    thread = std::thread(&HmiInterface::run, this);
}

void HmiInterface::close() {
    running = false;
    if (thread.joinable()) {
        thread.join();
        std::cout << "Thread joined sucessfully!" << std::endl;
    }
}

void HmiInterface::update() {
    
}

void HmiInterface::run() {
    while (running) {
        mutex.lock();
        server.check_received();
        mutex.unlock();

        // Update public Feedback and Control data
        Feedback = rx_data.Feedback;
        Control = rx_data.Control;
        
        if (update_data) {
            // Append new data to JSON log
            logger.Feedback.push_back(rx_data.Feedback);
            logger.Control.push_back(rx_data.Control);
        }
        
        
    }
}