import importlib
import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt
import json

import calib
importlib.reload(calib)


# Read experimental data
with open('em1500_wxyz.json', 'r') as f:

    data = json.load(f)

T = data['feedback']['t'][-1] - data['feedback']['t'][0]

t = np.array(data['feedback']['t']) - data['feedback']['t'][0]

eta = np.matrix(np.zeros([6, len(t)]))
eta_t = np.matrix(np.zeros([6, len(t)]))
v_mm = np.matrix(np.zeros([3, len(t)]))
a_mm = np.matrix(np.zeros([3, len(t)]))
w_mm = np.matrix(np.zeros([3, len(t)]))
w_bb = np.matrix(np.zeros([3, len(t)]))
phi_mru = np.matrix(np.zeros([3, len(t)]))

eta[0,:] = data['feedback']['em1500']['surge']
eta[1,:] = data['feedback']['em1500']['sway']
eta[2,:] = data['feedback']['em1500']['heave']
eta[3,:] = data['feedback']['em1500']['phi']
eta[4,:] = data['feedback']['em1500']['theta']
eta[5,:] = data['feedback']['em1500']['psi']

eta_t[0,:] = data['feedback']['em1500']['surge_t']
eta_t[1,:] = data['feedback']['em1500']['sway_t']
eta_t[2,:] = data['feedback']['em1500']['heave_t']

phi_t = np.zeros([3,1])
for i in range(0, len(t)):
    phi_t[0,0] = data['feedback']['em1500']['phi_t'][i]
    phi_t[1,0] = data['feedback']['em1500']['theta_t'][i]
    phi_t[2,0] = data['feedback']['em1500']['psi_t'][i]

    w_bb[:,i] = calib.Txyz(eta[3:6,i]).T.dot(phi_t)




# MRU data
v_mm[0,:] = data['feedback']['mru2']['x_t']
v_mm[1,:] = data['feedback']['mru2']['y_t']
v_mm[2,:] = data['feedback']['mru2']['z_t']

w_mm[0,:] = data['feedback']['mru2']['wx']
w_mm[1,:] = data['feedback']['mru2']['wy']
w_mm[2,:] = data['feedback']['mru2']['wz']

# plt.figure()
# plt.plot(t, w_mm[2,:].T)
# plt.plot(t, w_bb[2,:].T)
# plt.show()

x0 = [1.0, 0.0, 0.2, 0.0, 0.0, 0.0]
R, r = calib.solve_mru_pose(x0, t, eta, eta_t, w_bb, v_mm, w_mm, plot=True)


