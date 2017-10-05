import time
import numpy as np
import matplotlib.pyplot as plt
from build import motionlab as ml
import json



s = ml.RemoteInterface(50060)

s.start()


s.async_log(1)
time.sleep(20)

s.save_log('data.json')



s.close()


with open('data.json') as data_file:    
    data = json.load(data_file)


t = data['feedback']['t']

t = np.array(t)
t = t - t[0]

z = np.array(data['feedback']['em8000']['heave'])
z_t = np.array(data['feedback']['em8000']['heave_t'])
z_tt = np.array(data['feedback']['em8000']['heave_tt'])

plt.figure('position')
plt.plot(t,z)

plt.figure('velocity')
plt.plot(t,z_t)

plt.figure('acceleration')
plt.plot(t,z_tt)
plt.show()






