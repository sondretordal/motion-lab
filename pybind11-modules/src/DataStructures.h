#pragma once

#include <vector>
#include <iostream>

// Xbox data
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