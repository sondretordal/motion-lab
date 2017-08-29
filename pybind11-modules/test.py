import time
import numpy as np
import matplotlib.pyplot as plt
from build import MotionLab
import json



s = MotionLab.ShipSimulator()

s.start()
dt = 0.05
T = 10.0

t = []
z = []

tS = time.time()
while (time.time() - tS) <= T:
    # t.append(time.time() - tS)
    t.append(s.t)
    z.append(s.z)
    time.sleep(0.01)

s.close()

print t[-1]

plt.figure()
plt.plot(t, z)
plt.show()








