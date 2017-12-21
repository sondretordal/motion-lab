import numpy as np
import json
import importlib

# Calibration functions
import mru_calib
import park_martin
import kinematics as kin

importlib.reload(park_martin)

np.set_printoptions(precision=4, suppress=True)

# Empty dictionary
calib_data = {}

################################################################
# WORLD to EM8000
calib_data['WORLD_TO_EM8000'] = {}
calib_data['WORLD_TO_EM8000']['quat'] = [
        0.000060198987883,
        0.705931944115000,
        0.708279565403954,
        0.000379322138596
]

calib_data['WORLD_TO_EM8000']['pos'] = [
        -2.969661622702265,
        1.976311036084776,
        2.662845015592614
    ]

# WORLD to EM1500
calib_data['WORLD_TO_EM1500'] = {}
calib_data['WORLD_TO_EM1500']['quat'] = [
        0.000269356973877,
        -0.708291543794578,
        -0.705919386042796,
        -0.000914792257884
    ]

calib_data['WORLD_TO_EM1500']['pos'] = [
        0.391038069269004,
        -1.780959676838664,
        1.689612471594921
    ]

# EM8000 to EM1500
calib_data['EM8000_TO_EM1500'] = {}
calib_data['EM8000_TO_EM1500']['quat'] = [
        0.999994233253677,
        -0.000147371685366,
        0.000610386086891,
        0.003337539483092
    ]

calib_data['EM8000_TO_EM1500']['pos'] = [
        -3.768845951221771,
        3.347601117953204,
        0.973619107013598
    ]

# EM8000 to COMAU
calib_data['EM8000_TO_COMAU'] = {}
calib_data['EM8000_TO_COMAU']['quat'] = [
        0.002461288106714,
        -0.501408337431486,
        -0.865206982556575,
        0.000706081011787
    ]

calib_data['EM8000_TO_COMAU']['pos'] = [
        -1.082024099747949,
         1.536041691521612,
        -1.024461448780775
    ]


# EM8000 to MRU1
calib_data['EM8000_TO_MRU1'] = {}
calib_data['EM8000_TO_MRU1']['quat'] = [
        1.0,
        0.0,
        0.0,
        0.0
    ]

calib_data['EM8000_TO_MRU1']['pos'] = [
        -1.289,
        0.576,
        -0.966
    ]

# EM8000 to MRU1
calib_data['EM1500_TO_MRU2'] = {}
calib_data['EM1500_TO_MRU2']['quat'] = [
        1.0,
        0.0,
        0.0,
        0.0
    ]

calib_data['EM1500_TO_MRU2']['pos'] = [
        0.513,
        0.000,
        -0.169
    ]


################################################################

# Varying paramaters depending on calibration data
# EM8000 to AT960
with open('./data/at960_em8000.json') as fin:
    data = json.load(fin)

# Build H_at960 and H_em8000
H_at960 = []
H_em8000 = []
for i in range(0, len(data['feedback']['t'])):
    H =  np.eye(4)

    # AT960 data
    H[0:3,0:3] = kin.Rq([
            data['feedback']['at960']['q0'][i],
            data['feedback']['at960']['q1'][i],
            data['feedback']['at960']['q2'][i],
            data['feedback']['at960']['q3'][i]
        ])

    H[0:3,3] = np.array([
            data['feedback']['at960']['x'][i],
            data['feedback']['at960']['y'][i],
            data['feedback']['at960']['z'][i]
        ])

    H_at960.append(H.copy())
    
    # EM8000 data
    H[0:3,0:3] = kin.Rxyz([
            data['feedback']['em8000']['phi'][i],
            data['feedback']['em8000']['theta'][i],
            data['feedback']['em8000']['psi'][i]
        ])

    H[0:3,3] = np.array([
            data['feedback']['em8000']['surge'][i],
            data['feedback']['em8000']['sway'][i],
            data['feedback']['em8000']['heave'][i]
        ])

    H_em8000.append(H.copy())


# Build A and B matrices
A, B = [], []
for i in range(1, len(H_at960)):
    A.append(np.linalg.inv(H_em8000[i-1]).dot(H_em8000[i]))
    B.append(H_at960[i-1].dot(np.linalg.inv(H_at960[i])))

# Solve using Park Martin algorithm
R, t = park_martin.calibrate(A, B)

calib_data['EM8000_TO_AT960'] = {}
calib_data['EM8000_TO_AT960']['R'] = R.flatten().tolist()
calib_data['EM8000_TO_AT960']['t'] = t.tolist()


# EM1500 to TMAC
with open('./data/tmac_em1500.json') as fin:
    data = json.load(fin)

# Build H_at960 and H_em8000
H_at960 = []
H_em1500 = []
for i in range(0, len(data['feedback']['t'])):
    H =  np.eye(4)

    # AT960 data
    H[0:3,0:3] = kin.Rq([
            data['feedback']['at960']['q0'][i],
            data['feedback']['at960']['q1'][i],
            data['feedback']['at960']['q2'][i],
            data['feedback']['at960']['q3'][i]
        ])

    H[0:3,3] = np.array([
            data['feedback']['at960']['x'][i],
            data['feedback']['at960']['y'][i],
            data['feedback']['at960']['z'][i]
        ])

    H_at960.append(H.copy())
    
    # EM1500 data
    H[0:3,0:3] = kin.Rxyz([
            data['feedback']['em1500']['phi'][i],
            data['feedback']['em1500']['theta'][i],
            data['feedback']['em1500']['psi'][i]
        ])

    H[0:3,3] = np.array([
            data['feedback']['em1500']['surge'][i],
            data['feedback']['em1500']['sway'][i],
            data['feedback']['em1500']['heave'][i]
        ])

    H_em1500.append(H.copy())


# Build A and B matrices
A, B = [], []
for i in range(1, len(H_at960)):
    A.append(np.linalg.inv(H_em1500[i-1]).dot(H_em1500[i]))
    B.append(np.linalg.inv(H_at960[i-1]).dot(H_at960[i]))

# Solve using Park Martin algorithm
R, t = park_martin.calibrate(A, B)

calib_data['EM1500_TO_TMAC'] = {}


# EM1500 to ARUCO
calib_data['EM1500_TO_ARUCO'] = {}



# EM8000 to CAMERA
calib_data['EM8000_TO_CAMERA'] = {}


# Save calibration calib_data to json file
with open('calibration.json', 'w') as fout:
    json.dump(calib_data, fout, indent=4)
