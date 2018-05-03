#pragma once

#include <vector>
#include <iostream>

// Control structs
struct ControlComau {
	float q1 = 0.0f;
	float q2 = 0.0f;
	float q3 = 0.0f;
	float q4 = 0.0f;
	float q5 = 0.0f;
	float q6 = 0.0f;
	float q1_t = 0.0f;
	float q2_t = 0.0f;
	float q3_t = 0.0f;
	float q4_t = 0.0f;
	float q5_t = 0.0f;
	float q6_t = 0.0f;
	float q1_tt = 0.0f;
	float q2_tt = 0.0f;
	float q3_tt = 0.0f;
	float q4_tt = 0.0f;
	float q5_tt = 0.0f;
	float q6_tt = 0.0f;
};

struct Control {
	ControlComau comau;
};

// Feedback structs
struct Qtm3DMarkerPositionNoLabel {
	float x;
	float y;
	float z;
	int id;
};

struct FeedbackStewart {
	float surge;
	float sway;
	float heave;
	float phi;
	float theta;
	float psi;
	float surge_t;
	float sway_t;
	float heave_t;
	float phi_t;
	float theta_t;
	float psi_t;
	float surge_tt;
	float sway_tt;
	float heave_tt;
	float phi_tt;
	float theta_tt;
	float psi_tt;
};

struct FeedbackComau {
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

struct FeedbackLeica {
	float x;
	float y;
	float z;
	float q0;
	float q1;
	float q2;
	float q3;
};

struct FeedbackMru {
	float surge;
	float sway;
	float heave;
	float surge_t;
	float sway_t;
	float heave_t;
	float surge_tt;
	float sway_tt;
	float heave_tt;
	float turn_rate;
	float phi;
	float theta;
	float psi;
	float wx;
	float wy;
	float wz;
	float x_t;
	float y_t;
	float z_t;
	float x_tt;
	float y_tt;
	float z_tt;
};

struct FeedbackWinch {
	float l;
	float l_t;
	float l_tt;
};

struct Feedback {
	float t;
	FeedbackStewart em8000;
	FeedbackStewart em1500;
	FeedbackComau comau;
	FeedbackLeica at960;
	FeedbackMru mru1;
	FeedbackMru mru2;
	Qtm3DMarkerPositionNoLabel marker1;
	Qtm3DMarkerPositionNoLabel marker2;
	Qtm3DMarkerPositionNoLabel marker3;
	Qtm3DMarkerPositionNoLabel marker4;
	Qtm3DMarkerPositionNoLabel marker5;
	Qtm3DMarkerPositionNoLabel marker6;
	Qtm3DMarkerPositionNoLabel marker7;
	Qtm3DMarkerPositionNoLabel marker8;
	Qtm3DMarkerPositionNoLabel marker9;
	Qtm3DMarkerPositionNoLabel marker10;
	FeedbackWinch winch;
};

struct XboxData {
	float leftStickX;
    float leftStickY;
    float rightStickX;
    float rightStickY;
    float leftTrigger;
    float rightTrigger;

    bool buttonA = false;
    bool buttonB = false;
};