import time
import numpy as np
import matplotlib.pyplot as plt
from build import MotionLab
import json



rt = MotionLab.RemoteInterface(50060)


rt.start()



dt = 0.01
T = 5
N = int(T/dt)
tic = time.time()
rt.start_log()


for i in range(0, N):
    rt.Control.udp_key = i
    rt.update()
    time.sleep(dt)

rt.save_log('test.json')




rt.close()

file = open('test.json')

data = json.loads(file.read())

t = np.array(data['Feedback']['t'])
t = t - t[0]


z = np.array(data['Feedback']['EM8000']['z'])

plt.plot(t, z)
plt.show()






