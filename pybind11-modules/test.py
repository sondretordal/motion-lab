import time
import numpy as np
import matplotlib.pyplot as plt
from build import MotionLab
import json



s = MotionLab.ShipSimulator()


dt = 0.01
time = 0.0
T = 100.0
t = []
w = []
w2 = []
for i in range(0, int(T/dt)):
    s.simulate()
    w.append(s.z)

    w2.append(np.random.standard_normal())

    time = time + dt
    t.append(time)

plt.figure()
plt.plot(t, w)
plt.show()






