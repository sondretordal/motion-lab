#pragma once

#include <vector>
#include <iostream>

typedef std::array<float, 3> array_3;

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
	RemoteControlComau comau;
};

// Feedback structs
struct RemoteFeedbackStewart {
	float surge;
	float sway;
	float heave;
	float phi;
	float theta;
	float psi;
	float surge_t;
	float sway_t;
	float heave_t;
	float wx;
	float wy;
	float wz;
	float surge_tt;
	float sway_tt;
	float heave_tt;
	float wx_t;
	float wy_t;
	float wz_t;
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

struct RemoteFeedbackMru {
	float heave;
	float heave_t;
	float heave_tt;
	float turn_rate;
	float roll;
	float pitch;
	float yaw;
	float wx;
	float wy;
	float wz;
	float wx_t;
	float wy_t;
	float wz_t;
	float x_t;
	float y_t;
	float z_t;
	float x_tt;
	float y_tt;
	float z_tt;
};

struct RemoteFeedback {
	float t;
	RemoteFeedbackStewart em8000;
	RemoteFeedbackStewart em1500;
	RemoteFeedbackComau comau;
	RemoteFeedbackLeica at960;
	RemoteFeedbackMru mru1;
	RemoteFeedbackMru mru2;
};
