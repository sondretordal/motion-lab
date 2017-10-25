import numpy as np
from scipy import optimize
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt

def S(a):
    ax = a[0]
    ay = a[1]
    az = a[2]
    
    ret = np.array([[  0, -az,  ay],
                    [ az,   0, -ax],
                    [-ay,  ax,   0]])
    return ret

def Rx(x):
    ret = np.array([[ 1,         0,         0],
                    [ 0, np.cos(x),-np.sin(x)],
                    [ 0, np.sin(x), np.cos(x)]])
    return ret

def Ry(x):
    ret = np.array([[ np.cos(x), 0, np.sin(x)],
                    [         0, 1,         0],
                    [-np.sin(x), 0, np.cos(x)]])
    return ret

def Rz(x):
    ret = np.array([[ np.cos(x),-np.sin(x), 0],
                    [ np.sin(x), np.cos(x), 0],
                    [         0,         0, 1]])
    return ret

def Rxyz(phi):
    rx = phi[0]
    ry = phi[1]
    rz = phi[2]
    
    ret = Rx(rx).dot(Ry(ry)).dot(Rz(rz))

    return ret

def Txyz(phi):
    rx = phi[0]
    ry = phi[1]
    rz = phi[2]

    cy = np.cos(ry)
    sy = np.sin(ry)

    cz = np.cos(rz)
    sz = np.sin(rz)

    ret = np.array([[     cz,   -sz,  0],
                    [  cy*sz, cy*cz,  0],
                    [ -sy*cz, sy*sz, cy]])

    ret = 1.0/cy*ret

    return ret

def rot2euler(R):
    pitch = np.arcsin(R[0,2])
    roll = np.arcsin(-R[1,2]/np.cos(pitch))
    yaw = np.arcsin(-R[0,1]/np.cos(pitch))

    return np.array([roll, pitch,yaw])

def solve_mru_pose(x0, dt, t, body, mru, plot=False):
    # Interpolation data
    time = np.arange(t[0], t[-1], dt)

    phi = np.zeros([3, len(time)])
    phi[0,:] = interp1d(t, body['phi'])(time)
    phi[1,:] = interp1d(t, body['theta'])(time)
    phi[2,:] = interp1d(t, body['psi'])(time)

    phi_t = np.zeros([3, len(time)])
    phi_t[0,:] = interp1d(t, body['phi_t'])(time)
    phi_t[1,:] = interp1d(t, body['theta_t'])(time)
    phi_t[2,:] = interp1d(t, body['psi_t'])(time)

    v_mm = np.zeros([3, len(time)])
    v_mm[0,:] = interp1d(t, mru['x_t'])(time)
    v_mm[1,:] = interp1d(t, mru['y_t'])(time)
    v_mm[2,:] = interp1d(t, mru['z_t'])(time)

    w_mm = np.zeros([3, len(time)])
    w_mm[0,:] = interp1d(t, mru['wx'])(time)
    w_mm[1,:] = interp1d(t, mru['wy'])(time)
    w_mm[2,:] = interp1d(t, mru['wz'])(time)

    w_bb = np.zeros([3, len(time)])
    for i in range(0, len(time)):
        w_bb[:,i] = Txyz(phi[:,i]).T.dot(phi_t[:,i]).ravel()

    # Optimiziation objective functions
    def orientation(x, w_bb, w_mm):
        phi = np.array([x[0], x[1], x[2]])

        # Calculate squared sum error
        E = 0
        for i in range(0, len(time)):
            e = w_bb[:,i] - Rxyz(phi).dot(w_mm[:,i])
            E = E + e.T.dot(e)

        print('E = ', E)
        return E

    def position(x, R, w_bb, v_mm):
        r = np.array([x[0], x[1], x[2]])

        # Calculate squared sum error
        E = 0
        for i in range(0, len(time)):
            e = R.dot(v_mm[:,i]) - S(w_bb[:,i]).dot(r)

            E = E + e.T.dot(e)

        print('E = ', E)
        return E
    
    # Optimize unknown parameters
    f = lambda x: orientation(x, w_bb, w_mm)
    res1 = optimize.minimize(f, x0[0:3], tol=0.01)
    R = Rxyz(res1.x)
    print('*** Orientation Completed ***')

    f = lambda x: position(x, R, w_bb, v_mm)
    res2 = optimize.minimize(f, x0[3:6], tol=0.01)
    r = res2.x
    print('*** Position Completed ***')

    if plot:
        _w_mm = np.zeros(w_bb.shape)
        _v_mm = np.zeros(w_bb.shape)

        for i in range(len(time)):
            _w_mm[:,i] = R.T.dot(w_bb[:,i])
            _v_mm[:,i] = R.T.dot(S(w_bb[:,i])).dot(r)

        plt.close('all')
        plt.figure()

        plt.subplot(321)
        plt.plot(time, v_mm[0,:].T, 'r', label='mru')
        plt.plot(time, _v_mm[0,:].T, 'k--', label='transformed')
        plt.ylabel('x-velocity')
        plt.legend()

        plt.subplot(323)
        plt.plot(time, v_mm[1,:].T, 'r', label='mru')
        plt.plot(time, _v_mm[1,:].T, 'k--', label='transformed')
        plt.ylabel('y-velocity')
        plt.legend()

        plt.subplot(325)
        plt.plot(time, v_mm[2,:].T, 'r', label='mru')
        plt.plot(time, _v_mm[2,:].T, 'k--', label='transformed')
        plt.ylabel('z-velocity')
        plt.xlabel('Time - [s]')
        plt.legend()
        
        plt.subplot(322)
        plt.plot(time, w_mm[0,:].T, 'r', label='mru')
        plt.plot(time, _w_mm[0,:].T, 'k--', label='transformed')
        plt.ylabel('rx-velocity')
        plt.legend()
        plt.subplot(324)
        plt.plot(time, w_mm[1,:].T, 'g', label='mru')
        plt.plot(time, _w_mm[1,:].T, 'k--', label='transformed')
        plt.ylabel('ry-velocity')
        plt.legend()
        plt.subplot(326)
        plt.plot(time, w_mm[2,:].T, 'b', label='mru')
        plt.plot(time, _w_mm[2,:].T, 'k--', label='transformed')
        plt.ylabel('rz-velocity')
        plt.xlabel('Time - [s]')
        plt.legend()

        plt.show()

    return R, r