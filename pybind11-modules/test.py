import time
import numpy as np
import matplotlib.pyplot as plt
from build import MotionLab
import json



s = MotionLab.ShipSimulator()

s.start()

T = 240.0

t = []
x = []
y = []
z = []
roll = []
pitch = []
yaw = []

tS = time.time()
while (time.time() - tS) <= T:
    # t.append(time.time() - tS)
    t.append(s.t)

    x.append(s.x)
    y.append(s.y)
    z.append(s.z)
    roll.append(s.roll)
    pitch.append(s.pitch)
    yaw.append(s.yaw)

    time.sleep(0.1)

s.close()

print t[-1]

plt.figure()
plt.subplot(211)
plt.plot(t, x, 'r', label='Surge')
plt.plot(t, y, 'g', label='Sway')
plt.plot(t, z, 'b', label='Heave')
plt.grid()
plt.ylabel('Position - [m]')
plt.legend(loc=1)

plt.subplot(212)
plt.plot(t, np.array(roll)/np.pi*180, 'r', label='Roll')
plt.plot(t, np.array(pitch)/np.pi*180, 'g', label='Pitch')
plt.plot(t, np.array(yaw)/np.pi*180, 'b', label='Yaw')
plt.xlabel('Time - [s]')
plt.ylabel('Angle - [deg]')
plt.grid()
plt.legend(loc=1)

plt.show()







