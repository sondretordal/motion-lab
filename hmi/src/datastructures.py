from ctypes import Structure, c_float, c_int, c_uint

# PLC -> HMI
class TxHmiStewart(Structure):
    _fields_ = [
        ('status', c_int),
        ('eta', 6*c_float),
        ('eta_ref', 6*c_float),
        ('eta_sim', 6*c_float),
        ('cyl', 6*c_float)
    ]

class TxHmiComau(Structure):
    _fields_ = [
        ('status', c_int),
        ('q', 6*c_float)
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
        ('em8000', TxHmiStewart),
        ('em1500', TxHmiStewart),
        ('comau', TxHmiComau)
        # ('at960', TxHmiLeica),
        # ('mru1', TxHmiMru),
        # ('mru2', TxHmiMru)
    ]


