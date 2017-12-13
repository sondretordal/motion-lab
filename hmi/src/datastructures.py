from ctypes import Structure, c_float, c_int, c_uint

class TxHmiStewart(Structure):
    _fields_ = [
        ('status', c_int),
        ('u', 6*c_float),
        ('u_sim', 6*c_float),
        ('eta', 6*c_float),
        ('L', 6*c_float)
    ]

class TxHmiComau(Structure):
    _fields_ = [
        ('status', c_int),
        ('u', 6*c_float)
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

