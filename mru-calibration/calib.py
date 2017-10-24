import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt

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

def Rxyz(phi):
    rx = phi[0, 0]
    ry = phi[1, 0]
    rz = phi[2, 0]
    
    R = Rx(rx)*Ry(ry)*Rz(rz)

    return R

def Txyz(phi):
    rx = phi[0, 0]
    ry = phi[1, 0]
    rz = phi[2, 0]

    cy = np.cos(ry)
    sy = np.sin(ry)

    cz = np.cos(rz)
    sz = np.sin(rz)

    T = np.matrix([[     cz,   -sz,  0],
                   [  cy*sz, cy*cz,  0],
                   [ -sy*cz, sy*sz, cy]])

    T = 1.0/cy*T

    return T

def rot2euler(R):
    pitch = np.arcsin(R[0,2])
    roll = np.arcsin(-R[1,2]/np.cos(pitch))
    yaw = np.arcsin(-R[0,1]/np.cos(pitch))

    return np.matrix([roll, pitch,yaw]).T

def solve_mru_pose(x0, t, eta, eta_t, w_bb, v_mm, w_mm, plot=False):
    # Prepare data for pose optimization
    
    Rnb = []
    for i in range(eta.shape[1]):
        Rnb.append(Rxyz(eta[3:6,i]))

    def orientation(x, w_bb, w_mm):
        phi = np.matrix([x[0], x[1], x[2]]).T

        # Calculate error
        E = 0
        for i in range(0, w_mm.shape[1]):
            e = w_bb[:,i] - Rxyz(phi)*w_mm[:,i]
            E = E + e.T*e

        print('E = ', E[0,0])
        return E[0,0]

    def position(x, R, w_bb, v_mm):
        r = np.matrix([x[0], x[1], x[2]]).T

        # Calculate squared sum error
        E = 0
        for i in range(0, v_mm.shape[1]):
            e = R*v_mm[:,i] - S(w_bb[:,i])*r
            E = E + e.T*e

        print('E = ', E[0,0])
        return E[0,0]
    
    # Optimize unknown parameters
    f = lambda x: orientation(x, w_bb, w_mm)
    res1 = optimize.minimize(f, x0[0:3], tol=0.01)
    R = Rxyz(np.matrix(res1.x).T)
    print('*** Orientation Completed ***')

    f = lambda x: position(x, R, w_bb, v_mm)
    res2 = optimize.minimize(f, x0[3:6], tol=0.01)
    r = np.matrix(res2.x).T
    print('*** Position Completed ***')

    if plot:
        v = np.matrix(np.zeros(v_mm.shape))
        w = np.matrix(np.zeros(v_mm.shape))
        _eta_t = np.matrix(np.zeros(eta.shape))
        _w_bb = np.matrix(np.zeros(w_bb.shape))

        for i in range(v.shape[1]):
            v[:,i] = (Rnb[i]*R).T*(eta_t[0:3,i] + Rnb[i]*S(w_bb[:,i])*r)
            w[:,i] = R.T*w_bb[:,i]

            _eta_t[0:3,i] = Rnb[i]*R*v_mm[:,i] - Rnb[i]*S(w_bb[:,i])*r
            _w_bb[:,i] = R*w_mm[:,i]

        plt.close('all')
        plt.figure()

        plt.subplot(321)
        plt.plot(t, eta_t[0,:].T, 'r', label='stewart')
        plt.plot(t, _eta_t[0,:].T, 'k--', label='mru')
        plt.ylabel('x-velocity')
        plt.legend()
        plt.subplot(323)
        plt.plot(t, eta_t[1,:].T, 'g', label='stewart')
        plt.plot(t, _eta_t[1,:].T, 'k--', label='mru')
        plt.ylabel('y-velocity')
        plt.legend()
        plt.subplot(325)
        plt.plot(t, eta_t[2,:].T, 'b', label='stewart')
        plt.plot(t, _eta_t[2,:].T, 'k--', label='mru')
        plt.ylabel('z-velocity')
        plt.xlabel('Time - [s]')
        plt.legend()
        
        plt.subplot(322)
        plt.plot(t, w_bb[0,:].T, 'r', label='stewart')
        plt.plot(t, _w_bb[0,:].T, 'k--', label='mru')
        plt.ylabel('rx-velocity')
        plt.legend()
        plt.subplot(324)
        plt.plot(t, w_bb[1,:].T, 'g', label='stewart')
        plt.plot(t, _w_bb[1,:].T, 'k--', label='mru')
        plt.ylabel('ry-velocity')
        plt.legend()
        plt.subplot(326)
        plt.plot(t, w_bb[2,:].T, 'b', label='stewart')
        plt.plot(t, _w_bb[2,:].T, 'k--', label='mru')
        plt.ylabel('rz-velocity')
        plt.xlabel('Time - [s]')
        plt.legend()

        plt.show()

    return R, r