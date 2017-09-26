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

        json_log["feedback"]["em1500"]["surge"].push_back(feedback[i].em1500.surge);
        json_log["feedback"]["em1500"]["sway"].push_back(feedback[i].em1500.sway);
        json_log["feedback"]["em1500"]["heave"].push_back(feedback[i].em1500.heave);
        json_log["feedback"]["em1500"]["roll"].push_back(feedback[i].em1500.roll);
        json_log["feedback"]["em1500"]["pitch"].push_back(feedback[i].em1500.pitch);
        json_log["feedback"]["em1500"]["yaw"].push_back(feedback[i].em1500.yaw);
        json_log["feedback"]["em1500"]["surge_t"].push_back(feedback[i].em1500.surge_t);
        json_log["feedback"]["em1500"]["sway_t"].push_back(feedback[i].em1500.sway_t);
        json_log["feedback"]["em1500"]["heave_t"].push_back(feedback[i].em1500.heave_t);
        json_log["feedback"]["em1500"]["wx"].push_back(feedback[i].em1500.wx);
        json_log["feedback"]["em1500"]["wy"].push_back(feedback[i].em1500.wy);
        json_log["feedback"]["em1500"]["wz"].push_back(feedback[i].em1500.wz);
        json_log["feedback"]["em1500"]["surge_tt"].push_back(feedback[i].em1500.surge_tt);
        json_log["feedback"]["em1500"]["sway_tt"].push_back(feedback[i].em1500.sway_tt);
        json_log["feedback"]["em1500"]["heave_tt"].push_back(feedback[i].em1500.heave_tt);
        json_log["feedback"]["em1500"]["wx_t"].push_back(feedback[i].em1500.wx_t);
        json_log["feedback"]["em1500"]["wy_t"].push_back(feedback[i].em1500.wy_t);
        json_log["feedback"]["em1500"]["wz_t"].push_back(feedback[i].em1500.wz_t);
        json_log["feedback"]["em1500"]["L1"].push_back(feedback[i].em1500.L1);
        json_log["feedback"]["em1500"]["L2"].push_back(feedback[i].em1500.L2);
        json_log["feedback"]["em1500"]["L3"].push_back(feedback[i].em1500.L3);
        json_log["feedback"]["em1500"]["L4"].push_back(feedback[i].em1500.L4);
        json_log["feedback"]["em1500"]["L5"].push_back(feedback[i].em1500.L5);
        json_log["feedback"]["em1500"]["L6"].push_back(feedback[i].em1500.L6);
        
        json_log["feedback"]["em8000"]["surge"].push_back(feedback[i].em8000.surge);
        json_log["feedback"]["em8000"]["sway"].push_back(feedback[i].em8000.sway);
        json_log["feedback"]["em8000"]["heave"].push_back(feedback[i].em8000.heave);
        json_log["feedback"]["em8000"]["roll"].push_back(feedback[i].em8000.roll);
        json_log["feedback"]["em8000"]["pitch"].push_back(feedback[i].em8000.pitch);
        json_log["feedback"]["em8000"]["yaw"].push_back(feedback[i].em8000.yaw);
        json_log["feedback"]["em8000"]["surge_t"].push_back(feedback[i].em8000.surge_t);
        json_log["feedback"]["em8000"]["sway_t"].push_back(feedback[i].em8000.sway_t);
        json_log["feedback"]["em8000"]["heave_t"].push_back(feedback[i].em8000.heave_t);
        json_log["feedback"]["em8000"]["wx"].push_back(feedback[i].em8000.wx);
        json_log["feedback"]["em8000"]["wy"].push_back(feedback[i].em8000.wy);
        json_log["feedback"]["em8000"]["wz"].push_back(feedback[i].em8000.wz);
        json_log["feedback"]["em8000"]["surge_tt"].push_back(feedback[i].em8000.surge_tt);
        json_log["feedback"]["em8000"]["sway_tt"].push_back(feedback[i].em8000.sway_tt);
        json_log["feedback"]["em8000"]["heave_tt"].push_back(feedback[i].em8000.heave_tt);
        json_log["feedback"]["em8000"]["wx_t"].push_back(feedback[i].em8000.wx_t);
        json_log["feedback"]["em8000"]["wy_t"].push_back(feedback[i].em8000.wy_t);
        json_log["feedback"]["em8000"]["wz_t"].push_back(feedback[i].em8000.wz_t);
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

        json_log["feedback"]["mru1"]["heave"].push_back(feedback[i].mru1.heave);
        json_log["feedback"]["mru1"]["heave_t"].push_back(feedback[i].mru1.heave_t);
        json_log["feedback"]["mru1"]["heave_tt"].push_back(feedback[i].mru1.heave_tt);
        json_log["feedback"]["mru1"]["turn_rate"].push_back(feedback[i].mru1.turn_rate);
        json_log["feedback"]["mru1"]["roll"].push_back(feedback[i].mru1.roll);
        json_log["feedback"]["mru1"]["pitch"].push_back(feedback[i].mru1.pitch);
        json_log["feedback"]["mru1"]["yaw"].push_back(feedback[i].mru1.yaw);
        json_log["feedback"]["mru1"]["wx"].push_back(feedback[i].mru1.wx);
        json_log["feedback"]["mru1"]["wy"].push_back(feedback[i].mru1.wy);
        json_log["feedback"]["mru1"]["wz"].push_back(feedback[i].mru1.wz);
        json_log["feedback"]["mru1"]["wx_t"].push_back(feedback[i].mru1.wx_t);
        json_log["feedback"]["mru1"]["wy_t"].push_back(feedback[i].mru1.wy_t);
        json_log["feedback"]["mru1"]["wz_t"].push_back(feedback[i].mru1.wz_t);
        json_log["feedback"]["mru1"]["x_t"].push_back(feedback[i].mru1.x_t);
        json_log["feedback"]["mru1"]["y_t"].push_back(feedback[i].mru1.y_t);
        json_log["feedback"]["mru1"]["z_t"].push_back(feedback[i].mru1.z_t);
        json_log["feedback"]["mru1"]["x_tt"].push_back(feedback[i].mru1.x_tt);
        json_log["feedback"]["mru1"]["y_tt"].push_back(feedback[i].mru1.y_tt);
        json_log["feedback"]["mru1"]["z_tt"].push_back(feedback[i].mru1.z_tt);

        json_log["feedback"]["mru2"]["heave"].push_back(feedback[i].mru2.heave);
        json_log["feedback"]["mru2"]["heave_t"].push_back(feedback[i].mru2.heave_t);
        json_log["feedback"]["mru2"]["heave_tt"].push_back(feedback[i].mru2.heave_tt);
        json_log["feedback"]["mru2"]["turn_rate"].push_back(feedback[i].mru2.turn_rate);
        json_log["feedback"]["mru2"]["roll"].push_back(feedback[i].mru2.roll);
        json_log["feedback"]["mru2"]["pitch"].push_back(feedback[i].mru2.pitch);
        json_log["feedback"]["mru2"]["yaw"].push_back(feedback[i].mru2.yaw);
        json_log["feedback"]["mru2"]["wx"].push_back(feedback[i].mru2.wx);
        json_log["feedback"]["mru2"]["wy"].push_back(feedback[i].mru2.wy);
        json_log["feedback"]["mru2"]["wz"].push_back(feedback[i].mru2.wz);
        json_log["feedback"]["mru2"]["wx_t"].push_back(feedback[i].mru2.wx_t);
        json_log["feedback"]["mru2"]["wy_t"].push_back(feedback[i].mru2.wy_t);
        json_log["feedback"]["mru2"]["wz_t"].push_back(feedback[i].mru2.wz_t);
        json_log["feedback"]["mru2"]["x_t"].push_back(feedback[i].mru2.x_t);
        json_log["feedback"]["mru2"]["y_t"].push_back(feedback[i].mru2.y_t);
        json_log["feedback"]["mru2"]["z_t"].push_back(feedback[i].mru2.z_t);
        json_log["feedback"]["mru2"]["x_tt"].push_back(feedback[i].mru2.x_tt);
        json_log["feedback"]["mru2"]["y_tt"].push_back(feedback[i].mru2.y_tt);
        json_log["feedback"]["mru2"]["z_tt"].push_back(feedback[i].mru2.z_tt);

        json_log["feedback"]["ship1"]["surge"].push_back(feedback[i].ship1.surge);
        json_log["feedback"]["ship1"]["sway"].push_back(feedback[i].ship1.sway);
        json_log["feedback"]["ship1"]["heave"].push_back(feedback[i].ship1.heave);
        json_log["feedback"]["ship1"]["roll"].push_back(feedback[i].ship1.roll);
        json_log["feedback"]["ship1"]["pitch"].push_back(feedback[i].ship1.pitch);
        json_log["feedback"]["ship1"]["yaw"].push_back(feedback[i].ship1.yaw);

        json_log["feedback"]["ship2"]["surge"].push_back(feedback[i].ship2.surge);
        json_log["feedback"]["ship2"]["sway"].push_back(feedback[i].ship2.sway);
        json_log["feedback"]["ship2"]["heave"].push_back(feedback[i].ship2.heave);
        json_log["feedback"]["ship2"]["roll"].push_back(feedback[i].ship2.roll);
        json_log["feedback"]["ship2"]["pitch"].push_back(feedback[i].ship2.pitch);
        json_log["feedback"]["ship2"]["yaw"].push_back(feedback[i].ship2.yaw);
        
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