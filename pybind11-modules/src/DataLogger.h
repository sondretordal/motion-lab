#pragma once

#include <iostream>
#include <fstream>

#include "DataStructures.h"

// Json for modern C++
#include "json.hpp"

using json = nlohmann::json;

class DataLogger
{
private:
    std::ofstream file;

    json j;

public:
    DataLogger(std::string path) {
        file.open(path);
    }

    ~DataLogger() {};

    void save(LogData data) {
        if (data.Feedback.size() == data.Control.size()) {
            for (unsigned int i = 0; i < data.Feedback.size(); i++) {
                // Save Feedback data
                j["Feedback"]["t"].push_back(data.Feedback[i].t);
                
                j["Feedback"]["EM1500"]["x"].push_back(data.Feedback[i].EM1500.x);
                j["Feedback"]["EM1500"]["y"].push_back(data.Feedback[i].EM1500.y);
                j["Feedback"]["EM1500"]["z"].push_back(data.Feedback[i].EM1500.z);
                j["Feedback"]["EM1500"]["roll"].push_back(data.Feedback[i].EM1500.roll);
                j["Feedback"]["EM1500"]["pitch"].push_back(data.Feedback[i].EM1500.pitch);
                j["Feedback"]["EM1500"]["yaw"].push_back(data.Feedback[i].EM1500.yaw);
                j["Feedback"]["EM1500"]["x_t"].push_back(data.Feedback[i].EM1500.x_t);
                j["Feedback"]["EM1500"]["y_t"].push_back(data.Feedback[i].EM1500.y_t);
                j["Feedback"]["EM1500"]["z_t"].push_back(data.Feedback[i].EM1500.z_t);
                j["Feedback"]["EM1500"]["roll_t"].push_back(data.Feedback[i].EM1500.roll_t);
                j["Feedback"]["EM1500"]["pitch_t"].push_back(data.Feedback[i].EM1500.pitch_t);
                j["Feedback"]["EM1500"]["yaw_t"].push_back(data.Feedback[i].EM1500.yaw_t);
                j["Feedback"]["EM1500"]["x_tt"].push_back(data.Feedback[i].EM1500.x_tt);
                j["Feedback"]["EM1500"]["y_tt"].push_back(data.Feedback[i].EM1500.y_tt);
                j["Feedback"]["EM1500"]["z_tt"].push_back(data.Feedback[i].EM1500.z_tt);
                j["Feedback"]["EM1500"]["roll_tt"].push_back(data.Feedback[i].EM1500.roll_tt);
                j["Feedback"]["EM1500"]["pitch_tt"].push_back(data.Feedback[i].EM1500.pitch_tt);
                j["Feedback"]["EM1500"]["yaw_tt"].push_back(data.Feedback[i].EM1500.yaw_tt);
                j["Feedback"]["EM1500"]["L1"].push_back(data.Feedback[i].EM1500.L1);
                j["Feedback"]["EM1500"]["L2"].push_back(data.Feedback[i].EM1500.L2);
                j["Feedback"]["EM1500"]["L3"].push_back(data.Feedback[i].EM1500.L3);
                j["Feedback"]["EM1500"]["L4"].push_back(data.Feedback[i].EM1500.L4);
                j["Feedback"]["EM1500"]["L5"].push_back(data.Feedback[i].EM1500.L5);
                j["Feedback"]["EM1500"]["L6"].push_back(data.Feedback[i].EM1500.L6);

                j["Feedback"]["EM8000"]["x"].push_back(data.Feedback[i].EM8000.x);
                j["Feedback"]["EM8000"]["y"].push_back(data.Feedback[i].EM8000.y);
                j["Feedback"]["EM8000"]["z"].push_back(data.Feedback[i].EM8000.z);
                j["Feedback"]["EM8000"]["roll"].push_back(data.Feedback[i].EM8000.roll);
                j["Feedback"]["EM8000"]["pitch"].push_back(data.Feedback[i].EM8000.pitch);
                j["Feedback"]["EM8000"]["yaw"].push_back(data.Feedback[i].EM8000.yaw);
                j["Feedback"]["EM8000"]["x_t"].push_back(data.Feedback[i].EM8000.x_t);
                j["Feedback"]["EM8000"]["y_t"].push_back(data.Feedback[i].EM8000.y_t);
                j["Feedback"]["EM8000"]["z_t"].push_back(data.Feedback[i].EM8000.z_t);
                j["Feedback"]["EM8000"]["roll_t"].push_back(data.Feedback[i].EM8000.roll_t);
                j["Feedback"]["EM8000"]["pitch_t"].push_back(data.Feedback[i].EM8000.pitch_t);
                j["Feedback"]["EM8000"]["yaw_t"].push_back(data.Feedback[i].EM8000.yaw_t);
                j["Feedback"]["EM8000"]["x_tt"].push_back(data.Feedback[i].EM8000.x_tt);
                j["Feedback"]["EM8000"]["y_tt"].push_back(data.Feedback[i].EM8000.y_tt);
                j["Feedback"]["EM8000"]["z_tt"].push_back(data.Feedback[i].EM8000.z_tt);
                j["Feedback"]["EM8000"]["roll_tt"].push_back(data.Feedback[i].EM8000.roll_tt);
                j["Feedback"]["EM8000"]["pitch_tt"].push_back(data.Feedback[i].EM8000.pitch_tt);
                j["Feedback"]["EM8000"]["yaw_tt"].push_back(data.Feedback[i].EM8000.yaw_tt);
                j["Feedback"]["EM8000"]["L1"].push_back(data.Feedback[i].EM8000.L1);
                j["Feedback"]["EM8000"]["L2"].push_back(data.Feedback[i].EM8000.L2);
                j["Feedback"]["EM8000"]["L3"].push_back(data.Feedback[i].EM8000.L3);
                j["Feedback"]["EM8000"]["L4"].push_back(data.Feedback[i].EM8000.L4);
                j["Feedback"]["EM8000"]["L5"].push_back(data.Feedback[i].EM8000.L5);
                j["Feedback"]["EM8000"]["L6"].push_back(data.Feedback[i].EM8000.L6);

                j["Feedback"]["COMAU"]["q1"].push_back(data.Feedback[i].COMAU.q1);
                j["Feedback"]["COMAU"]["q2"].push_back(data.Feedback[i].COMAU.q2);
                j["Feedback"]["COMAU"]["q3"].push_back(data.Feedback[i].COMAU.q3);
                j["Feedback"]["COMAU"]["q4"].push_back(data.Feedback[i].COMAU.q4);
                j["Feedback"]["COMAU"]["q5"].push_back(data.Feedback[i].COMAU.q5);
                j["Feedback"]["COMAU"]["q6"].push_back(data.Feedback[i].COMAU.q6);
                j["Feedback"]["COMAU"]["q1_t"].push_back(data.Feedback[i].COMAU.q1_t);
                j["Feedback"]["COMAU"]["q2_t"].push_back(data.Feedback[i].COMAU.q2_t);
                j["Feedback"]["COMAU"]["q3_t"].push_back(data.Feedback[i].COMAU.q3_t);
                j["Feedback"]["COMAU"]["q4_t"].push_back(data.Feedback[i].COMAU.q4_t);
                j["Feedback"]["COMAU"]["q5_t"].push_back(data.Feedback[i].COMAU.q5_t);
                j["Feedback"]["COMAU"]["q6_t"].push_back(data.Feedback[i].COMAU.q6_t);
                j["Feedback"]["COMAU"]["q1_tt"].push_back(data.Feedback[i].COMAU.q1_tt);
                j["Feedback"]["COMAU"]["q2_tt"].push_back(data.Feedback[i].COMAU.q2_tt);
                j["Feedback"]["COMAU"]["q3_tt"].push_back(data.Feedback[i].COMAU.q3_tt);
                j["Feedback"]["COMAU"]["q4_tt"].push_back(data.Feedback[i].COMAU.q4_tt);
                j["Feedback"]["COMAU"]["q5_tt"].push_back(data.Feedback[i].COMAU.q5_tt);
                j["Feedback"]["COMAU"]["q6_tt"].push_back(data.Feedback[i].COMAU.q6_tt);

                j["Feedback"]["AT960"]["x"].push_back(data.Feedback[i].AT960.x);
                j["Feedback"]["AT960"]["y"].push_back(data.Feedback[i].AT960.y);
                j["Feedback"]["AT960"]["z"].push_back(data.Feedback[i].AT960.z);
                j["Feedback"]["AT960"]["q0"].push_back(data.Feedback[i].AT960.q0);
                j["Feedback"]["AT960"]["q1"].push_back(data.Feedback[i].AT960.q1);
                j["Feedback"]["AT960"]["q2"].push_back(data.Feedback[i].AT960.q2);
                j["Feedback"]["AT960"]["q3"].push_back(data.Feedback[i].AT960.q3);
                
                // Save Control data
                j["Control"]["COMAU"]["q1"].push_back(data.Control[i].COMAU.q1);
                j["Control"]["COMAU"]["q2"].push_back(data.Control[i].COMAU.q2);
                j["Control"]["COMAU"]["q3"].push_back(data.Control[i].COMAU.q3);
                j["Control"]["COMAU"]["q4"].push_back(data.Control[i].COMAU.q4);
                j["Control"]["COMAU"]["q5"].push_back(data.Control[i].COMAU.q5);
                j["Control"]["COMAU"]["q6"].push_back(data.Control[i].COMAU.q6);
                j["Control"]["COMAU"]["q1_t"].push_back(data.Control[i].COMAU.q1_t);
                j["Control"]["COMAU"]["q2_t"].push_back(data.Control[i].COMAU.q2_t);
                j["Control"]["COMAU"]["q3_t"].push_back(data.Control[i].COMAU.q3_t);
                j["Control"]["COMAU"]["q4_t"].push_back(data.Control[i].COMAU.q4_t);
                j["Control"]["COMAU"]["q5_t"].push_back(data.Control[i].COMAU.q5_t);
                j["Control"]["COMAU"]["q6_t"].push_back(data.Control[i].COMAU.q6_t);
                j["Control"]["COMAU"]["q1_tt"].push_back(data.Control[i].COMAU.q1_tt);
                j["Control"]["COMAU"]["q2_tt"].push_back(data.Control[i].COMAU.q2_tt);
                j["Control"]["COMAU"]["q3_tt"].push_back(data.Control[i].COMAU.q3_tt);
                j["Control"]["COMAU"]["q4_tt"].push_back(data.Control[i].COMAU.q4_tt);
                j["Control"]["COMAU"]["q5_tt"].push_back(data.Control[i].COMAU.q5_tt);
                j["Control"]["COMAU"]["q6_tt"].push_back(data.Control[i].COMAU.q6_tt);
            }
        } else {
            std::cout << "Error: Control/Feedback dimension mismatch" << std::endl;
            exit(EXIT_FAILURE);
        }
    }

    void close() {
        file << std::setw(4) << j << std::endl;

        file.close();
    }
};



