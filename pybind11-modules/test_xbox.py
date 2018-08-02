import time
from build import motionlab as ml




xbox = ml.XboxController()

xbox.start()

while xbox.is_connected():
    
    if abs(xbox.LT) > 0.0:
        print('xbox.LT', xbox.LT)

    if abs(xbox.RT) > 0.0:
        print('xbox.RT', xbox.RT)

    if abs(xbox.right.x) > 0.0:
        print('xbox.right.x', xbox.right.x)

    if abs(xbox.right.y) > 0.0:
        print('xbox.right.y', xbox.right.y)

    if abs(xbox.left.x) > 0.0:
        print('xbox.left.x', xbox.left.x)

    if abs(xbox.left.y) > 0.0:
        print('xbox.left.y', xbox.left.y)

    if abs(xbox.left.clicked) > 0.0:
        print('xbox.left.clicked')

    if abs(xbox.right.clicked) > 0.0:
        print('xbox.right.clicked')

    if xbox.A:
        print('A Pressed')

    if xbox.B:
        print('B Pressed')

    if xbox.X:
        print('X Pressed')

    if xbox.Y:
        print('Y Pressed')

    if xbox.menu:
        print('menu Pressed')
    
    if xbox.LB:
        print('LB Pressed')

    if xbox.RB:
        print('RB Pressed')

    if xbox.joypad.up:
        print('joypad.up Pressed')
    
    if xbox.joypad.down:
        print('joypad.down Pressed')

    if xbox.joypad.left:
        print('joypad.left Pressed')

    if xbox.joypad.right:
        print('joypad.right Pressed')

    xbox.vibrate(abs(xbox.left.x), abs(xbox.right.x))


    time.sleep(0.05)

    if xbox.back:
        xbox.close()

        xbox.battery_level()

        break





