#include "HmiInterface.h"

#include "HmiInterface.h"


HmiInterface::HmiInterface(unsigned int port) :
thread(), logger(), server(port, &rx_data, sizeof(rx_data), &tx_data, sizeof(tx_data)) {

}

HmiInterface::~HmiInterface() {
    close();
    clear_log();
}

void HmiInterface::start_log(std::string update_rate) {
    ms_rate = static_cast<unsigned int>(std::stoi(update_rate));
    logging = true;
}

void HmiInterface::clear_log() {
    logging = false;
    logger.clear();
}
void HmiInterface::save_log(std::string path) {
    logging = false;
    logger.save(path);
    logger.clear();
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

        // Update ms_counter
        ms_counter++;
      
        // Update public feedback and control data
        feedback = rx_data.feedback;
        rx_data.control = control;
        
        if (logging && (ms_counter >= ms_rate)) {
            // Append new data to JSON log
            logger.feedback.push_back(rx_data.feedback);
            logger.control.push_back(rx_data.control);

            ms_counter = 0;
        }
    }
}