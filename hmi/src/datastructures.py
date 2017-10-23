from ctypes import Structure, c_float, c_int, c_uint

class TxHmiStewart(Structure):
    _fields_ = [
        ('status', c_int),
        ('surge', c_float),
        ('sway', c_float),
        ('heave', c_float),
        ('phi', c_float),
        ('theta', c_float),
        ('psi', c_float),
        ('surge_ref', c_float),
        ('sway_ref', c_float),
        ('heave_ref', c_float),
        ('phi_ref', c_float),
        ('theta_ref', c_float),
        ('psi_ref', c_float),
        ('L1', c_float),
        ('L2', c_float),
        ('L3', c_float),
        ('L4', c_float),
        ('L5', c_float),
        ('L6', c_float)
    ]

class TxHmiComau(Structure):
    _fields_ = [
        ('status', c_int),
        ('q1', c_float),
        ('q2', c_float),
        ('q3', c_float),
        ('q4', c_float),
        ('q5', c_float),
        ('q6', c_float)
    ]

class TxHmiLeica(Structure):
    _fields_ = [
        ('status', c_int),
        ('x', c_float),
        ('y', c_float),
        ('z', c_float),
        ('q0', c_float),
        ('q1', c_float),
        ('q2', c_float),
        ('q3', c_float)
    ]

class TxHmiMru(Structure):
    _fields_ = [
        ('status', c_int)
    ]

class TxHmi(Structure):
    _fields_ = [
        ('t', c_float),
        ('em8000', TxHmiStewart),
        ('em1500', TxHmiStewart),
        ('comau', TxHmiComau),
        ('at960', TxHmiLeica),
        ('mru1', TxHmiMru),
        ('mru2', TxHmiMru)
    ]

