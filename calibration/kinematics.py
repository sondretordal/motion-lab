import numpy as np

def Rq(q):
    Q = q/np.linalg.norm(q)
    
    q0 = Q[0]
    qX = Q[1]
    qY = Q[2]
    qZ = Q[3]
    
    R = np.zeros([3, 3])
    
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

    return Rx(phi[0]).dot(Ry(phi[1])).dot(Rz(phi[2]))