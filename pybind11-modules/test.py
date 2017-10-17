import time
import numpy as np
import matplotlib.pyplot as plt
from build import motionlab as ml
import json

def S(a):
    ax = a[0, 0]
    ay = a[1, 0]
    az = a[2, 0]
    
    ret = np.matrix([[  0, -az,  ay],
                     [ az,   0, -ax],
                     [-ay,  ax,   0]])
    return ret

def Rx(x):
    ret = np.matrix([[ 1,         0,         0],
                     [ 0, np.cos(x),-np.sin(x)],
                     [ 0, np.sin(x), np.cos(x)]])
    return ret

def Ry(x):
    ret = np.matrix([[ np.cos(x), 0, np.sin(x)],
                     [         0, 1,         0],
                     [-np.sin(x), 0, np.cos(x)]])
    return ret

def Rz(x):
    ret = np.matrix([[ np.cos(x),-np.sin(x), 0],
                     [ np.sin(x), np.cos(x), 0],
                     [         0,         0, 1]])
    return ret

def Rq(q):
    Q = q/np.linalg.norm(q)
    
    q0 = Q[0, 0]
    qX = Q[1, 0]
    qY = Q[2, 0]
    qZ = Q[3, 0]
    
    R = np.matrix(np.zeros([3, 3]))
    
    R[0,0] = 1 - 2*qY**2 - 2*qZ**2
    R[1,0] = 2*(qX*qY  + qZ*q0)
    R[2,0] = 2*(qX*qZ - qY*q0)
    
    R[0,1] = 2*(qX*qY - qZ*q0)
    R[1,1] = 1 - 2*qX**2 - 2*qZ**2
    R[2,1] = 2*(qY*qZ + qX*q0)
    
    R[0,2] = 2*(qX*qZ + qY*q0)
    R[1,2] = 2*(qY*qZ - qX*q0)
    R[2,2] = 1 - 2*qX**2 - 2*qY**2
    
    return R

def Rxyz(phi):
    rx = phi[0]
    ry = phi[1]
    rz = phi[2]
    
    R = Rx(rx)*Ry(ry)*Rz(rz)

    return R

def Txyz(phi):
    rx = phi[0]
    ry = phi[1]
    rz = phi[2]

    cy = np.cos(ry)
    sy = np.sin(ry)

    cz = np.cos(rz)
    sz = np.sin(rz)

    T = np.matrix([[     cz,   -sz,  0],
                   [  cy*sz, cy*cz,  0],
                   [ -sy*cz, sy*sz, cy]])

    T = 1.0/cy*T

    return T

# s = ml.RemoteInterface(50060)
# s.start()
# s.async_log(1)
# time.sleep(40)
# s.save_log('data.json')
# s.close()

with open('data.json') as data_file:    
    data = json.load(data_file)

t = data['feedback']['t']

t = np.matrix(t)
t = t - t[0]


phi = np.matrix(np.zeros([3, len(t)]))
w =  np.matrix(np.zeros([3, len(t)]))
phi_t =  np.matrix(np.zeros([3, len(t)]))
m_phi_t =  np.matrix(np.zeros([3, len(t)]))

phi[0,:] = np.matrix(data['feedback']['em8000']['pitch'])
phi[1,:] = np.matrix(data['feedback']['em8000']['roll'])
phi[2,:] = np.matrix(data['feedback']['em8000']['yaw'])

w[0,:] = np.matrix(data['feedback']['em8000']['wx'])
w[1,:] = np.matrix(data['feedback']['em8000']['wy'])
w[2,:] = np.matrix(data['feedback']['em8000']['wz'])

for i in range(0, len(t)):
    m_phi_t[:,i] = Txyz(phi[:,i])*w[:,i]


for i in range(1, len(t)):
    dt = t[i]-t[i-1]
    phi_t[:,i] = (phi[:,i] - phi[:,i-1])/dt

    
plt.figure()
plt.plot(t, m_phi_t[0,:].T, 'r')
plt.plot(t, phi_t[0,:].T, 'b')

plt.show()




