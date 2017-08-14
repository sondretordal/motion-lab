#pragma once

#include <iostream>
#include <cstdint>
#include <fstream>

#include "DataStructures.h"

// Json for modern C++  
#include "json.hpp"

class JsonLogger
{
private:
    // Log file
    std::ofstream file;

    // Json file
    nlohmann::json json_log;
public:
    std::vector<RemoteFeedback> feedback;
    std::vector<RemoteControl> control;

    JsonLogger();
    ~JsonLogger();

    void save(std::string path);
    void clear();
};



