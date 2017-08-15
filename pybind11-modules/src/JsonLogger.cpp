#include "JsonLogger.h"

JsonLogger::JsonLogger() {
    clear();
}

JsonLogger::~JsonLogger() {
    clear();
}

void JsonLogger::clear() {
    feedback.clear();
    control.clear();
    json_log.clear();
}

void JsonLogger::save(std::string path) {
    for (unsigned int i = 0; i < feedback.size(); i++) {
        // Save feedback data
        json_log["feedback"]["t"].push_back(feedback[i].t);

        json_log["feedback"]["em1500"]["x"].push_back(feedback[i].em1500.x);
        json_log["feedback"]["em1500"]["y"].push_back(feedback[i].em1500.y);
        json_log["feedback"]["em1500"]["z"].push_back(feedback[i].em1500.z);
        json_log["feedback"]["em1500"]["roll"].push_back(feedback[i].em1500.roll);
        json_log["feedback"]["em1500"]["pitch"].push_back(feedback[i].em1500.pitch);
        json_log["feedback"]["em1500"]["yaw"].push_back(feedback[i].em1500.yaw);
        json_log["feedback"]["em1500"]["x_t"].push_back(feedback[i].em1500.x_t);
        json_log["feedback"]["em1500"]["y_t"].push_back(feedback[i].em1500.y_t);
        json_log["feedback"]["em1500"]["z_t"].push_back(feedback[i].em1500.z_t);
        json_log["feedback"]["em1500"]["roll_t"].push_back(feedback[i].em1500.roll_t);
        json_log["feedback"]["em1500"]["pitch_t"].push_back(feedback[i].em1500.pitch_t);
        json_log["feedback"]["em1500"]["yaw_t"].push_back(feedback[i].em1500.yaw_t);
        json_log["feedback"]["em1500"]["x_tt"].push_back(feedback[i].em1500.x_tt);
        json_log["feedback"]["em1500"]["y_tt"].push_back(feedback[i].em1500.y_tt);
        json_log["feedback"]["em1500"]["z_tt"].push_back(feedback[i].em1500.z_tt);
        json_log["feedback"]["em1500"]["roll_tt"].push_back(feedback[i].em1500.roll_tt);
        json_log["feedback"]["em1500"]["pitch_tt"].push_back(feedback[i].em1500.pitch_tt);
        json_log["feedback"]["em1500"]["yaw_tt"].push_back(feedback[i].em1500.yaw_tt);
        json_log["feedback"]["em1500"]["L1"].push_back(feedback[i].em1500.L1);
        json_log["feedback"]["em1500"]["L2"].push_back(feedback[i].em1500.L2);
        json_log["feedback"]["em1500"]["L3"].push_back(feedback[i].em1500.L3);
        json_log["feedback"]["em1500"]["L4"].push_back(feedback[i].em1500.L4);
        json_log["feedback"]["em1500"]["L5"].push_back(feedback[i].em1500.L5);
        json_log["feedback"]["em1500"]["L6"].push_back(feedback[i].em1500.L6);

        json_log["feedback"]["em8000"]["x"].push_back(feedback[i].em8000.x);
        json_log["feedback"]["em8000"]["y"].push_back(feedback[i].em8000.y);
        json_log["feedback"]["em8000"]["z"].push_back(feedback[i].em8000.z);
        json_log["feedback"]["em8000"]["roll"].push_back(feedback[i].em8000.roll);
        json_log["feedback"]["em8000"]["pitch"].push_back(feedback[i].em8000.pitch);
        json_log["feedback"]["em8000"]["yaw"].push_back(feedback[i].em8000.yaw);
        json_log["feedback"]["em8000"]["x_t"].push_back(feedback[i].em8000.x_t);
        json_log["feedback"]["em8000"]["y_t"].push_back(feedback[i].em8000.y_t);
        json_log["feedback"]["em8000"]["z_t"].push_back(feedback[i].em8000.z_t);
        json_log["feedback"]["em8000"]["roll_t"].push_back(feedback[i].em8000.roll_t);
        json_log["feedback"]["em8000"]["pitch_t"].push_back(feedback[i].em8000.pitch_t);
        json_log["feedback"]["em8000"]["yaw_t"].push_back(feedback[i].em8000.yaw_t);
        json_log["feedback"]["em8000"]["x_tt"].push_back(feedback[i].em8000.x_tt);
        json_log["feedback"]["em8000"]["y_tt"].push_back(feedback[i].em8000.y_tt);
        json_log["feedback"]["em8000"]["z_tt"].push_back(feedback[i].em8000.z_tt);
        json_log["feedback"]["em8000"]["roll_tt"].push_back(feedback[i].em8000.roll_tt);
        json_log["feedback"]["em8000"]["pitch_tt"].push_back(feedback[i].em8000.pitch_tt);
        json_log["feedback"]["em8000"]["yaw_tt"].push_back(feedback[i].em8000.yaw_tt);
        json_log["feedback"]["em8000"]["L1"].push_back(feedback[i].em8000.L1);
        json_log["feedback"]["em8000"]["L2"].push_back(feedback[i].em8000.L2);
        json_log["feedback"]["em8000"]["L3"].push_back(feedback[i].em8000.L3);
        json_log["feedback"]["em8000"]["L4"].push_back(feedback[i].em8000.L4);
        json_log["feedback"]["em8000"]["L5"].push_back(feedback[i].em8000.L5);
        json_log["feedback"]["em8000"]["L6"].push_back(feedback[i].em8000.L6);

        json_log["feedback"]["comau"]["q1"].push_back(feedback[i].comau.q1);
        json_log["feedback"]["comau"]["q2"].push_back(feedback[i].comau.q2);
        json_log["feedback"]["comau"]["q3"].push_back(feedback[i].comau.q3);
        json_log["feedback"]["comau"]["q4"].push_back(feedback[i].comau.q4);
        json_log["feedback"]["comau"]["q5"].push_back(feedback[i].comau.q5);
        json_log["feedback"]["comau"]["q6"].push_back(feedback[i].comau.q6);
        json_log["feedback"]["comau"]["q1_t"].push_back(feedback[i].comau.q1_t);
        json_log["feedback"]["comau"]["q2_t"].push_back(feedback[i].comau.q2_t);
        json_log["feedback"]["comau"]["q3_t"].push_back(feedback[i].comau.q3_t);
        json_log["feedback"]["comau"]["q4_t"].push_back(feedback[i].comau.q4_t);
        json_log["feedback"]["comau"]["q5_t"].push_back(feedback[i].comau.q5_t);
        json_log["feedback"]["comau"]["q6_t"].push_back(feedback[i].comau.q6_t);
        json_log["feedback"]["comau"]["q1_tt"].push_back(feedback[i].comau.q1_tt);
        json_log["feedback"]["comau"]["q2_tt"].push_back(feedback[i].comau.q2_tt);
        json_log["feedback"]["comau"]["q3_tt"].push_back(feedback[i].comau.q3_tt);
        json_log["feedback"]["comau"]["q4_tt"].push_back(feedback[i].comau.q4_tt);
        json_log["feedback"]["comau"]["q5_tt"].push_back(feedback[i].comau.q5_tt);
        json_log["feedback"]["comau"]["q6_tt"].push_back(feedback[i].comau.q6_tt);

        json_log["feedback"]["at960"]["x"].push_back(feedback[i].at960.x);
        json_log["feedback"]["at960"]["y"].push_back(feedback[i].at960.y);
        json_log["feedback"]["at960"]["z"].push_back(feedback[i].at960.z);
        json_log["feedback"]["at960"]["q0"].push_back(feedback[i].at960.q0);
        json_log["feedback"]["at960"]["q1"].push_back(feedback[i].at960.q1);
        json_log["feedback"]["at960"]["q2"].push_back(feedback[i].at960.q2);
        json_log["feedback"]["at960"]["q3"].push_back(feedback[i].at960.q3);
        
        // Save control data
        json_log["control"]["comau"]["q1"].push_back(control[i].comau.q1);
        json_log["control"]["comau"]["q2"].push_back(control[i].comau.q2);
        json_log["control"]["comau"]["q3"].push_back(control[i].comau.q3);
        json_log["control"]["comau"]["q4"].push_back(control[i].comau.q4);
        json_log["control"]["comau"]["q5"].push_back(control[i].comau.q5);
        json_log["control"]["comau"]["q6"].push_back(control[i].comau.q6);
        json_log["control"]["comau"]["q1_t"].push_back(control[i].comau.q1_t);
        json_log["control"]["comau"]["q2_t"].push_back(control[i].comau.q2_t);
        json_log["control"]["comau"]["q3_t"].push_back(control[i].comau.q3_t);
        json_log["control"]["comau"]["q4_t"].push_back(control[i].comau.q4_t);
        json_log["control"]["comau"]["q5_t"].push_back(control[i].comau.q5_t);
        json_log["control"]["comau"]["q6_t"].push_back(control[i].comau.q6_t);
        json_log["control"]["comau"]["q1_tt"].push_back(control[i].comau.q1_tt);
        json_log["control"]["comau"]["q2_tt"].push_back(control[i].comau.q2_tt);
        json_log["control"]["comau"]["q3_tt"].push_back(control[i].comau.q3_tt);
        json_log["control"]["comau"]["q4_tt"].push_back(control[i].comau.q4_tt);
        json_log["control"]["comau"]["q5_tt"].push_back(control[i].comau.q5_tt);
        json_log["control"]["comau"]["q6_tt"].push_back(control[i].comau.q6_tt);
    }

    // Write json data to .json text file
    file.open(path);
    file << std::setw(4) << json_log << std::endl;
    file.close();

    // Clear log buffers
    clear();
}