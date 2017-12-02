#pragma once

// https://katyscode.wordpress.com/2013/08/30/xinput-tutorial-part-1-adding-gamepad-support-to-your-windows-game/

// We need the Windows Header and the XInput Header
#include <windows.h>
#include <iostream>
#include <cmath>
#include <chrono>
#include <thread>
#include <mutex>
#include <XInput.h>

#include "DataStructures.h"

// Now, the XInput Library
// NOTE: COMMENT THIS OUT IF YOU ARE NOT USING
// A COMPILER THAT SUPPORTS THIS METHOD OF LINKING LIBRARIES
#pragma comment(lib, "XInput.lib")


struct Stick
{
    float x = 0.0f;
    float y = 0.0f;
    bool clicked = false;
};

struct Joypad
{
    bool up = false;
    bool down = false;
    bool left = false;
    bool right = false;
};

// XBOX Controller Class Definition
class XboxController
{
private:
    int cId;
    XINPUT_STATE state;
    
    // Thread related
	std::thread thread;
	std::mutex mutex;
    bool running = false;
    void run();

    // Deadzone settings
    float deadzoneX = 0.1f;
    float deadzoneY = 0.1f;
 
public:
    // Constructor and destructor
    XboxController();
    ~XboxController();
    
    // Joystick
    Stick left, right;

    // Joypad
    Joypad joypad;

    // Triggers
    float LT = 0.0f;
    float RT = 0.0f;

    // Buttons only
    bool A = false;
    bool B = false;
    bool X = false;
    bool Y = false;
    bool LB = false;
    bool RB = false;
    bool back = false;
    bool menu = false;
    
    void start();
    void close();
    bool update();
    void vibrate(float left, float right);
    bool is_connected();
    void battery_level();
    
};