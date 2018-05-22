#include "JsonLogger.h"

JsonLogger::JsonLogger() {
    clear();
}

JsonLogger::~JsonLogger() {
    clear();
}

void JsonLogger::clear() {

}

void JsonLogger::save(std::string path) {
    // Write json data to .json text file
    file.open(path);
    file << std::setw(4) << json_log << std::endl;
    file.close();

    // Clear log buffers
    clear();
}