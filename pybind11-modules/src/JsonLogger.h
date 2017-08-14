#pragma once

#include <iostream>
#include <cstdint>
#include <fstream>

#include "DataStructures.h"

// Json for modern C++  
#include "json.hpp"
using json = nlohmann::json;

class JsonLogger
{
private:
    // Log file
    std::ofstream file;

    // Json file
    json j, j2;
public:
    std::vector<RemoteFeedback> feedback;
    std::vector<RemoteControl> control;

    JsonLogger() {
        clear();
    }

    ~JsonLogger() {
        clear();
    };

    void clear() {
        feedback.clear();
        control.clear();
    }

    void save(std::string path) {
        for (unsigned int i = 0; i < feedback.size(); i++) {
            // Save feedback data
            j["feedback"]["t"].push_back(feedback[i].t);

            j["feedback"]["em1500"]["x"].push_back(feedback[i].em1500.x);
            j["feedback"]["em1500"]["y"].push_back(feedback[i].em1500.y);
            j["feedback"]["em1500"]["z"].push_back(feedback[i].em1500.z);
            j["feedback"]["em1500"]["roll"].push_back(feedback[i].em1500.roll);
            j["feedback"]["em1500"]["pitch"].push_back(feedback[i].em1500.pitch);
            j["feedback"]["em1500"]["yaw"].push_back(feedback[i].em1500.yaw);
            j["feedback"]["em1500"]["x_t"].push_back(feedback[i].em1500.x_t);
            j["feedback"]["em1500"]["y_t"].push_back(feedback[i].em1500.y_t);
            j["feedback"]["em1500"]["z_t"].push_back(feedback[i].em1500.z_t);
            j["feedback"]["em1500"]["roll_t"].push_back(feedback[i].em1500.roll_t);
            j["feedback"]["em1500"]["pitch_t"].push_back(feedback[i].em1500.pitch_t);
            j["feedback"]["em1500"]["yaw_t"].push_back(feedback[i].em1500.yaw_t);
            j["feedback"]["em1500"]["x_tt"].push_back(feedback[i].em1500.x_tt);
            j["feedback"]["em1500"]["y_tt"].push_back(feedback[i].em1500.y_tt);
            j["feedback"]["em1500"]["z_tt"].push_back(feedback[i].em1500.z_tt);
            j["feedback"]["em1500"]["roll_tt"].push_back(feedback[i].em1500.roll_tt);
            j["feedback"]["em1500"]["pitch_tt"].push_back(feedback[i].em1500.pitch_tt);
            j["feedback"]["em1500"]["yaw_tt"].push_back(feedback[i].em1500.yaw_tt);
            j["feedback"]["em1500"]["L1"].push_back(feedback[i].em1500.L1);
            j["feedback"]["em1500"]["L2"].push_back(feedback[i].em1500.L2);
            j["feedback"]["em1500"]["L3"].push_back(feedback[i].em1500.L3);
            j["feedback"]["em1500"]["L4"].push_back(feedback[i].em1500.L4);
            j["feedback"]["em1500"]["L5"].push_back(feedback[i].em1500.L5);
            j["feedback"]["em1500"]["L6"].push_back(feedback[i].em1500.L6);

            j["feedback"]["em8000"]["x"].push_back(feedback[i].em8000.x);
            j["feedback"]["em8000"]["y"].push_back(feedback[i].em8000.y);
            j["feedback"]["em8000"]["z"].push_back(feedback[i].em8000.z);
            j["feedback"]["em8000"]["roll"].push_back(feedback[i].em8000.roll);
            j["feedback"]["em8000"]["pitch"].push_back(feedback[i].em8000.pitch);
            j["feedback"]["em8000"]["yaw"].push_back(feedback[i].em8000.yaw);
            j["feedback"]["em8000"]["x_t"].push_back(feedback[i].em8000.x_t);
            j["feedback"]["em8000"]["y_t"].push_back(feedback[i].em8000.y_t);
            j["feedback"]["em8000"]["z_t"].push_back(feedback[i].em8000.z_t);
            j["feedback"]["em8000"]["roll_t"].push_back(feedback[i].em8000.roll_t);
            j["feedback"]["em8000"]["pitch_t"].push_back(feedback[i].em8000.pitch_t);
            j["feedback"]["em8000"]["yaw_t"].push_back(feedback[i].em8000.yaw_t);
            j["feedback"]["em8000"]["x_tt"].push_back(feedback[i].em8000.x_tt);
            j["feedback"]["em8000"]["y_tt"].push_back(feedback[i].em8000.y_tt);
            j["feedback"]["em8000"]["z_tt"].push_back(feedback[i].em8000.z_tt);
            j["feedback"]["em8000"]["roll_tt"].push_back(feedback[i].em8000.roll_tt);
            j["feedback"]["em8000"]["pitch_tt"].push_back(feedback[i].em8000.pitch_tt);
            j["feedback"]["em8000"]["yaw_tt"].push_back(feedback[i].em8000.yaw_tt);
            j["feedback"]["em8000"]["L1"].push_back(feedback[i].em8000.L1);
            j["feedback"]["em8000"]["L2"].push_back(feedback[i].em8000.L2);
            j["feedback"]["em8000"]["L3"].push_back(feedback[i].em8000.L3);
            j["feedback"]["em8000"]["L4"].push_back(feedback[i].em8000.L4);
            j["feedback"]["em8000"]["L5"].push_back(feedback[i].em8000.L5);
            j["feedback"]["em8000"]["L6"].push_back(feedback[i].em8000.L6);

            j["feedback"]["comau"]["q1"].push_back(feedback[i].comau.q1);
            j["feedback"]["comau"]["q2"].push_back(feedback[i].comau.q2);
            j["feedback"]["comau"]["q3"].push_back(feedback[i].comau.q3);
            j["feedback"]["comau"]["q4"].push_back(feedback[i].comau.q4);
            j["feedback"]["comau"]["q5"].push_back(feedback[i].comau.q5);
            j["feedback"]["comau"]["q6"].push_back(feedback[i].comau.q6);
            j["feedback"]["comau"]["q1_t"].push_back(feedback[i].comau.q1_t);
            j["feedback"]["comau"]["q2_t"].push_back(feedback[i].comau.q2_t);
            j["feedback"]["comau"]["q3_t"].push_back(feedback[i].comau.q3_t);
            j["feedback"]["comau"]["q4_t"].push_back(feedback[i].comau.q4_t);
            j["feedback"]["comau"]["q5_t"].push_back(feedback[i].comau.q5_t);
            j["feedback"]["comau"]["q6_t"].push_back(feedback[i].comau.q6_t);
            j["feedback"]["comau"]["q1_tt"].push_back(feedback[i].comau.q1_tt);
            j["feedback"]["comau"]["q2_tt"].push_back(feedback[i].comau.q2_tt);
            j["feedback"]["comau"]["q3_tt"].push_back(feedback[i].comau.q3_tt);
            j["feedback"]["comau"]["q4_tt"].push_back(feedback[i].comau.q4_tt);
            j["feedback"]["comau"]["q5_tt"].push_back(feedback[i].comau.q5_tt);
            j["feedback"]["comau"]["q6_tt"].push_back(feedback[i].comau.q6_tt);

            j["feedback"]["at960"]["x"].push_back(feedback[i].at960.x);
            j["feedback"]["at960"]["y"].push_back(feedback[i].at960.y);
            j["feedback"]["at960"]["z"].push_back(feedback[i].at960.z);
            j["feedback"]["at960"]["q0"].push_back(feedback[i].at960.q0);
            j["feedback"]["at960"]["q1"].push_back(feedback[i].at960.q1);
            j["feedback"]["at960"]["q2"].push_back(feedback[i].at960.q2);
            j["feedback"]["at960"]["q3"].push_back(feedback[i].at960.q3);
            
            // Save control data
            j["control"]["comau"]["q1"].push_back(control[i].comau.q1);
            j["control"]["comau"]["q2"].push_back(control[i].comau.q2);
            j["control"]["comau"]["q3"].push_back(control[i].comau.q3);
            j["control"]["comau"]["q4"].push_back(control[i].comau.q4);
            j["control"]["comau"]["q5"].push_back(control[i].comau.q5);
            j["control"]["comau"]["q6"].push_back(control[i].comau.q6);
            j["control"]["comau"]["q1_t"].push_back(control[i].comau.q1_t);
            j["control"]["comau"]["q2_t"].push_back(control[i].comau.q2_t);
            j["control"]["comau"]["q3_t"].push_back(control[i].comau.q3_t);
            j["control"]["comau"]["q4_t"].push_back(control[i].comau.q4_t);
            j["control"]["comau"]["q5_t"].push_back(control[i].comau.q5_t);
            j["control"]["comau"]["q6_t"].push_back(control[i].comau.q6_t);
            j["control"]["comau"]["q1_tt"].push_back(control[i].comau.q1_tt);
            j["control"]["comau"]["q2_tt"].push_back(control[i].comau.q2_tt);
            j["control"]["comau"]["q3_tt"].push_back(control[i].comau.q3_tt);
            j["control"]["comau"]["q4_tt"].push_back(control[i].comau.q4_tt);
            j["control"]["comau"]["q5_tt"].push_back(control[i].comau.q5_tt);
            j["control"]["comau"]["q6_tt"].push_back(control[i].comau.q6_tt);
        }

        // Write json data to .json text file
        file.open(path);
        //std::vector<std::uint8_t> v_cbor = json::to_cbor(j);
        
        //file.write((char*)&v_cbor[0], v_cbor.size()*sizeof(uint8_t));
        file << std::setw(4) << j << std::endl;
        file.close();

        clear();
    };
};



