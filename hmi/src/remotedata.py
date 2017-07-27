from ctypes import Structure, c_uint, c_float

# RX data
class RxStewart(Structure):
    _pack_ = 1
    _fields_ = [
        ('x', c_float),
        ('y', c_float),
        ('z', c_float),
        ('roll', c_float),
        ('pitch', c_float),
        ('yaw', c_float),
        ('x_t', c_float),
        ('y_t', c_float),
        ('z_t', c_float),
        ('roll_t', c_float),
        ('pitch_t', c_float),
        ('yaw_t', c_float),
        ('x_tt', c_float),
        ('y_tt', c_float),
        ('z_tt', c_float),
        ('roll_tt', c_float),
        ('pitch_tt', c_float),
        ('yaw_tt', c_float),
        ('L1', c_float),
        ('L2', c_float),
        ('L3', c_float),
        ('L4', c_float),
        ('L5', c_float),
        ('L6', c_float)
    ]

class RxComau(Structure):
    _pack_ = 1
    _fields_ = [
        ('q1', c_float),
        ('q2', c_float),
        ('q3', c_float),
        ('q4', c_float),
        ('q5', c_float),
        ('q6', c_float),
        ('q1_t', c_float),
        ('q2_t', c_float),
        ('q3_t', c_float),
        ('q4_t', c_float),
        ('q5_t', c_float),
        ('q6_t', c_float),
        ('q1_tt', c_float),
        ('q2_tt', c_float),
        ('q3_tt', c_float),
        ('q4_tt', c_float),
        ('q5_tt', c_float),
        ('q6_tt', c_float)
    ]

class RxLeica(Structure):
    _pack_ = 1
    _fields_ = [
        ('x', c_float),
        ('y', c_float),
        ('z', c_float),
        ('q0', c_float),
        ('q1', c_float),
        ('q2', c_float),
        ('q3', c_float)
    ]

class RxData(Structure):
    _pack_ = 1
    _fields_ = [
        ('t', c_float),
        ('EM1500', RxStewart),
        ('EM8000', RxStewart),
        ('COMAU', RxComau),
        ('AT960', RxLeica)
    ]

# TX data
class TxData(Structure):
    _pack_ = 1
    _fields_ = [
        ('udpKey',c_uint)
    ]