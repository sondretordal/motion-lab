import numpy as np
import json

# Calibration functions
import park_martin
import mru_calib

# Empty dictionary
calib_data = {}

################################################################
# WORLD to EM8000
calib_data['WORLD_TO_EM8000'] = {}
calib_data['WORLD_TO_EM8000']['R'] = [
        -0.003320173308196, 0.999994295495463, 0.000620826655442,
         0.999994386834698, 0.003319892785463, 0.000452339461846,
         0.000450275803539, 0.000622325016046,-0.999999704981594
    ]

calib_data['WORLD_TO_EM8000']['t'] = [
        -2.969661622702265,
         1.976311036084776,
         2.662845015592614
    ]

# WORLD to EM1500
calib_data['WORLD_TO_EM1500'] = {}
calib_data['WORLD_TO_EM1500']['R'] = [
        0.003353967128172, 0.999993956280895, 0.000915590621924,
        0.999992970658198,-0.003355495711564, 0.001673105711803,
        0.001676167860428, 0.000909972644365,-0.999998181203891
    ]

calib_data['WORLD_TO_EM1500']['t'] = [
         0.391038069269004,
        -1.780959676838664,
         1.689612471594921
    ]

# EM8000 to EM1500
calib_data['EM8000_TO_EM1500'] = {}
calib_data['EM8000_TO_EM1500']['R'] = [
         0.999976976518048,-0.006675220379950, 0.001219781416261,
         0.006674860565444, 0.999977678223570, 0.000298816046351,
        -0.001221748851535,-0.000290667295691, 0.999999211420823
    ]

calib_data['EM8000_TO_EM1500']['t'] = [
        -3.768845951221771,
         3.347601117953204,
         0.973619107013598
    ]

# EM8000 to COMAU
calib_data['EM8000_TO_COMAU'] = {}
calib_data['EM8000_TO_COMAU']['R'] = [
        -0.497167242430097, 0.867640513578017,-0.004967117124449,
         0.867647465053204, 0.497178361207596, 0.001246408311757,
         0.003550977499601,-0.003690033198352,-0.999986887020921
    ]

calib_data['EM8000_TO_COMAU']['t'] = [
        -1.082024099747949,
         1.536041691521612,
        -1.024461448780775
    ]
################################################################

# EM8000 to MRU1
with open('./data/mru_calib_em8000.json') as fin:
    data = json.load(fin)

calib_data['EM8000_TO_MRU1'] = {}
x0 = [-0.5, 0.5, -0.5, 0, 0, 0]
R, t = mru_calib.optimize_mru_pose(
        x0, 
        0.1, 
        data['feedback']['t'], 
        data['feedback']['em8000'],
        data['feedback']['mru1'],
        plot=True
    )

print(R)
print(t)

calib_data['EM8000_TO_MRU1'] = {}
calib_data['EM8000_TO_MRU1']['R'] = R.flatten().tolist()
calib_data['EM8000_TO_MRU1']['t'] = t.tolist()

# EM1500 to MRU2
with open('./data/mru_calib_em1500.json') as fin:
    data = json.load(fin)

x0 = [0.5, 0, -0.2, 0, 0, 0]
R, t = mru_calib.optimize_mru_pose(
        x0, 
        0.1, 
        data['feedback']['t'], 
        data['feedback']['em1500'],
        data['feedback']['mru2'],
        plot=True
    )

calib_data['EM1500_TO_MRU2'] = {}
calib_data['EM1500_TO_MRU2']['R'] = R.flatten().tolist()
calib_data['EM1500_TO_MRU2']['t'] = t.tolist()


# Varying paramaters depending on calibration calib_data
# EM1500 to PROBE
calib_data['EM1500_TO_PROBE'] = {}

# EM1500 to ARUCO
calib_data['EM1500_TO_ARUCO'] = {}

# EM8000 to AT960
calib_data['EM8000_TO_AT960'] = {}

# EM8000 to CAMERA
calib_data['EM8000_TO_CAMERA'] = {}


# Save calibration calib_data to json file
with open('calibration.json', 'w') as fout:
    json.dump(calib_data, fout, indent=4)
