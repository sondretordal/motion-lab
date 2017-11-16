import numpy as np

# http://folk.ntnu.no/torstem/snippets/robcam_calibration.html#park_martinpy

def log(R):
    # Rotation matrix logarithm
    theta = np.arccos((R[0,0] + R[1,1] + R[2,2] - 1.0)/2.0)
    return np.array([R[2,1] - R[1,2], R[0,2] - R[2,0], R[1,0] - R[0,1]]) * theta / (2*np.sin(theta))

def invsqrt(mat):
    u,s,v = np.linalg.svd(mat)
    return u.dot(np.diag(1.0/np.sqrt(s))).dot(v)

def calibrate(A, B):
    # Transform pairs A_i, B_i
    N = len(A)

    M = np.zeros([3,3])
    for i in range(N):
        Ra = A[i][0:3, 0:3]
        Rb = B[i][0:3, 0:3]

        M += np.outer(log(Rb), log(Ra))

    # Resulting rotation matrix
    Rx = np.dot(invsqrt(np.dot(M.T, M)), M.T)

    C = np.zeros([3*N, 3])
    d = np.zeros([3*N, 1])
    for i in range(N):
        Ra = A[i][0:3, 0:3]
        ta = A[i][0:3, 3]

        Rb = B[i][0:3, 0:3]
        tb = B[i][0:3, 3]
        
        C[3*i:3*i+3, :] = np.eye(3) - Ra
        d[3*i:3*i+3, 0] = ta - Rx.dot(tb)
        
    # Check matrix inversion condition. CLose to 1 is good!
    print("Matrix inversion condition: ", np.linalg.cond(np.dot(C.T, C)))
    
    # Solve LS problem
    tx = np.dot(np.linalg.inv(np.dot(C.T, C)), np.dot(C.T, d))
    return Rx, tx.flatten()