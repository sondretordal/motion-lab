#pragma once

#include <iostream>
#include <fstream>

#include "DataStructures.h"

struct Test {
    float t = 3.14f;
    float x = 10.0f;
    float y = -1.2345f;
};

class DataLogger
{
private:
    std::ofstream file;

    Test data;

public:
    DataLogger(std::string name) {
        file.open(name);

        file
        << "Time [s] \t"
        << "Test.x [m] \t"
        << "Test.y [m] \n";

    };

    ~DataLogger() {};

    void save() {
        file
        << data.t << "\t"
        << data.x << "\t"
        << data.y << "\n";
    }

    void close() {
        file.close();
    }
};



