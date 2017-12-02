#include "XboxController.h"

XboxController::XboxController() : thread()
{   
    // Check if Xbox controller is connected
    if ( !is_connected() )
    {
        std::cout << "Xbox controller is NOT connected!" << std::endl;
    }
}

XboxController::~XboxController()
{
    close();
}

bool XboxController::is_connected()
{
    int controllerId = -1;
    
    for (DWORD i = 0; i < XUSER_MAX_COUNT && controllerId == -1; i++)
    {
        XINPUT_STATE state;
        ZeroMemory(&state, sizeof(XINPUT_STATE));
        
    if (XInputGetState(i, &state) == ERROR_SUCCESS)
        controllerId = i;
    }
    
    cId = controllerId;
    
    return controllerId != -1;
}
 
// Returns false if the controller has been disconnected
bool XboxController::update()
{
    if (cId == -1)
        is_connected();

    if (cId != -1)
    {
        ZeroMemory(&state, sizeof(XINPUT_STATE));

        if (XInputGetState(cId, &state) != ERROR_SUCCESS)
        {
            cId = -1;
            return false;
        }
    
        float normLX = fmaxf(-1, (float) state.Gamepad.sThumbLX / 32767);
        float normLY = fmaxf(-1, (float) state.Gamepad.sThumbLY / 32767);
        
        left.x = (abs(normLX) < deadzoneX ? 0 : (abs(normLX) - deadzoneX) * (normLX / abs(normLX)));
        left.y = (abs(normLY) < deadzoneY ? 0 : (abs(normLY) - deadzoneY) * (normLY / abs(normLY)));
        
        if (deadzoneX > 0) left.x *= 1 / (1 - deadzoneX);
        if (deadzoneY > 0) left.y *= 1 / (1 - deadzoneY);
        
        float normRX = fmaxf(-1, (float) state.Gamepad.sThumbRX / 32767);
        float normRY = fmaxf(-1, (float) state.Gamepad.sThumbRY / 32767);
        
        right.x = (abs(normRX) < deadzoneX ? 0 : (abs(normRX) - deadzoneX) * (normRX / abs(normRX)));
        right.y = (abs(normRY) < deadzoneY ? 0 : (abs(normRY) - deadzoneY) * (normRY / abs(normRY)));
        
        if (deadzoneX > 0) right.x *= 1 / (1 - deadzoneX);
        if (deadzoneY > 0) right.y *= 1 / (1 - deadzoneY);
        
        LT = (float) state.Gamepad.bLeftTrigger / 255;
        RT = (float) state.Gamepad.bRightTrigger / 255;
        
        // Buttons
        left.clicked = (state.Gamepad.wButtons & XINPUT_GAMEPAD_LEFT_THUMB) != 0;
        right.clicked = (state.Gamepad.wButtons & XINPUT_GAMEPAD_RIGHT_THUMB) != 0; 

        joypad.up = (state.Gamepad.wButtons & XINPUT_GAMEPAD_DPAD_UP) != 0;
        joypad.down = (state.Gamepad.wButtons & XINPUT_GAMEPAD_DPAD_DOWN) != 0;
        joypad.left = (state.Gamepad.wButtons & XINPUT_GAMEPAD_DPAD_LEFT) != 0;
        joypad.right = (state.Gamepad.wButtons & XINPUT_GAMEPAD_DPAD_RIGHT) != 0;

        A = (state.Gamepad.wButtons & XINPUT_GAMEPAD_A) != 0;
        B = (state.Gamepad.wButtons & XINPUT_GAMEPAD_B) != 0;
        X = (state.Gamepad.wButtons & XINPUT_GAMEPAD_X) != 0;
        Y = (state.Gamepad.wButtons & XINPUT_GAMEPAD_Y) != 0;
        LB = (state.Gamepad.wButtons & XINPUT_GAMEPAD_LEFT_SHOULDER) != 0;
        RB = (state.Gamepad.wButtons & XINPUT_GAMEPAD_RIGHT_SHOULDER) != 0;
        back = (state.Gamepad.wButtons & XINPUT_GAMEPAD_BACK) != 0;
        menu = (state.Gamepad.wButtons & XINPUT_GAMEPAD_START) != 0;
        
        return true;
        }

    return false;
}

void XboxController::battery_level()
{
    // Create a battery state
    XINPUT_BATTERY_INFORMATION battery;

    // Zerooise the battery
    ZeroMemory(&battery, sizeof(XINPUT_BATTERY_INFORMATION));

    // Read battery info
    XInputGetBatteryInformation(cId, 0, &battery);

    // Print battery level
    switch (battery.BatteryLevel)
    {
    case BATTERY_LEVEL_EMPTY:
        std::cout << "Battery is empty! " << std::endl;
        break;

    case BATTERY_LEVEL_LOW:
        std::cout << "Battery is low! " << std::endl;
        break;

    case BATTERY_LEVEL_MEDIUM:
        std::cout << "Battery is medium! " << std::endl;
        break;

    case BATTERY_LEVEL_FULL:
        std::cout << "Battery is full! " << std::endl;
    }
}


void XboxController::vibrate(float left, float right)
{
    // Create a vibraton State
    XINPUT_VIBRATION vibration;

    // Zeroise the vibration
    ZeroMemory(&vibration, sizeof(XINPUT_VIBRATION));

    // Set the vibration Values
    vibration.wLeftMotorSpeed = static_cast<int>(left*65535.0f);
    vibration.wRightMotorSpeed = static_cast<int>(right*65535.0f);

    // Vibrate the controller
    XInputSetState(cId, &vibration);
}

void XboxController::run()
{
    while (running)
    {   
        // Update member fields
        mutex.lock();
        update();
        mutex.unlock();

        // Halt update rate
        std::this_thread::sleep_for(std::chrono::milliseconds(10));
    }
}

void XboxController::start()
{
    running = true;
    thread = std::thread(&XboxController::run, this);
}

void XboxController::close() {
    running = false;
    
    if (thread.joinable()) {
        thread.join();
    }
}
