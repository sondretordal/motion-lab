#pragma once

#include <iostream>
#include <vector>

// Control structs
struct RemoteControlComau {
	float q1;
	float q2;
	float q3;
	float q4;
	float q5;
	float q6;
	float q1_t;
	float q2_t;
	float q3_t;
	float q4_t;
	float q5_t;
	float q6_t;
	float q1_tt;
	float q2_tt;
	float q3_tt;
	float q4_tt;
	float q5_tt;
	float q6_tt;
};

struct RemoteControl {
	int	udp_key;
	RemoteControlComau COMAU;
};

// Feedback structs
struct RemoteFeedbackStewart {
	float x;
	float y;
	float z;
	float roll;
	float pitch;
	float yaw;
	float x_t;
	float y_t;
	float z_t;
	float roll_t;
	float pitch_t;
	float yaw_t;
	float x_tt;
	float y_tt;
	float z_tt;
	float roll_tt;
	float pitch_tt;
	float yaw_tt;
	float L1;
	float L2;
	float L3;
	float L4;
	float L5;
	float L6;
};

struct RemoteFeedbackComau {
	float q1;
	float q2;
	float q3;
	float q4;
	float q5;
	float q6;
	float q1_t;
	float q2_t;
	float q3_t;
	float q4_t;
	float q5_t;
	float q6_t;
	float q1_tt;
	float q2_tt;
	float q3_tt;
	float q4_tt;
	float q5_tt;
	float q6_tt;
};

struct RemoteFeedbackLeica {
	float x;
	float y;
	float z;
	float q0;
	float q1;
	float q2;
	float q3;
};

struct RemoteFeedback {
	float t;
	RemoteFeedbackStewart EM1500;
	RemoteFeedbackStewart EM8000;
	RemoteFeedbackComau COMAU;
	RemoteFeedbackLeica AT960;
};

// HMI data structures
struct HmiFeedback {
	RemoteControl Control;
	RemoteFeedback Feedback;
};

struct HmiControl {
	unsigned int counter;
};

// JSON logg data;
struct LogData {
	std::vector<RemoteControl> Control;
	std::vector<RemoteFeedback> Feedback;
};