#pragma once

// https://katyscode.wordpress.com/2013/08/30/xinput-tutorial-part-1-adding-gamepad-support-to-your-windows-game/

// We need the Windows Header and the XInput Header
#include <windows.h>
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
    void Run();

    // Deadzone settings
    const float deadzoneX;
    const float deadzoneY;
 
public:
    XboxController() : thread(), deadzoneX(0.02f), deadzoneY(0.02f) {}
    ~XboxController() {}
    
    float leftStickX;
    float leftStickY;
    float rightStickX;
    float rightStickY;
    float leftTrigger;
    float rightTrigger;

    bool buttonA = false;
    bool buttonB = false;
    
    void Start();
    void Close();

    XINPUT_GAMEPAD *GetState();
    int  GetPort();
    bool CheckConnection();
    bool Update();
    bool IsPressed(WORD button);

    bool ButtonA();
    bool ButtonB();
    bool ButtonX();
    bool ButtonY();
    bool ButtonBack();
    bool ButtonStart();

};