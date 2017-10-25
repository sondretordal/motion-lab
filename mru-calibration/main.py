import importlib
import numpy as np
import json

import calib
importlib.reload(calib)


with open('em1500.json', 'r') as f:
    data = json.load(f)

# Original time vector shifted to zero
t = np.array(data['feedback']['t']) - data['feedback']['t'][0]

# Body data
body = data['feedback']['em1500']
mru = data['feedback']['mru2']

# Calibrate position and orientation
dt = 0.01
x0 = [1, 0, 0.2, 0, 0, 0]
R, r = calib.solve_mru_pose(x0, dt, t, body, mru, plot=True)


