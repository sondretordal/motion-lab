from numpy import array, cos, sin, tan, identity

def Txyz(d):
    T = identity(4)
    T[0:3,3] = d

    return T


def Rxyz(phi):
    rx = phi[0]
    ry = phi[1]
    rz = phi[2]

    R = identity(4)
    R[0:3,0:3] = array([
        [                           cos(ry)*cos(rz),                          -cos(ry)*sin(rz),          sin(ry)],
        [ cos(rx)*sin(rz) + cos(rz)*sin(rx)*sin(ry), cos(rx)*cos(rz) - sin(rx)*sin(ry)*sin(rz), -cos(ry)*sin(rx)],
        [ sin(rx)*sin(rz) - cos(rx)*cos(rz)*sin(ry), cos(rz)*sin(rx) + cos(rx)*sin(ry)*sin(rz),  cos(rx)*cos(ry)]
    ])
    return R

def Rzyx(phi):
    rx = phi[0]
    ry = phi[1]
    rz = phi[2]

    R = identity(4)
    R[0:3,0:3] = array([
        [ cos(ry)*cos(rz), cos(rz)*sin(rx)*sin(ry) - cos(rx)*sin(rz), sin(rx)*sin(rz) + cos(rx)*cos(rz)*sin(ry)],
        [ cos(ry)*sin(rz), cos(rx)*cos(rz) + sin(rx)*sin(ry)*sin(rz), cos(rx)*sin(ry)*sin(rz) - cos(rz)*sin(rx)],
        [        -sin(ry),                           cos(ry)*sin(rx),                           cos(rx)*cos(ry)]
    ])
    return R

def InvH(H):
    R = H[0:3,0:3]
    t = H[0:3,3]

    invH = identity(4)

    invH[0:3,0:3] = R.transpose()
    invH[0:3,3] = -R.transpose().dot(t)

    return invH

# Denavit-Hartenberg
def DH(theta, d, a, alpha):
    '''
    Deneavit-Hartenberg transformation matrix
    ''' 
    return array([
        [ cos(theta),-sin(theta)*cos(alpha), sin(theta)*sin(alpha), a*cos(theta)],
        [ sin(theta), cos(theta)*cos(alpha),-cos(theta)*sin(alpha), a*sin(theta)],
        [ 0         , sin(alpha)           , cos(alpha)           , d           ],
        [ 0         , 0                    , 0                    , 1           ]
    ])
