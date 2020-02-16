from ctypes import Structure, c_float, c_int, c_uint, c_bool, c_uint8


# PLC -> HMI
class TxHmiStewart(Structure):
    _fields_ = [
        ('status', c_int),
        ('eta', 6*c_float),
        ('etaRef', 6*c_float),
        ('etaSim', 6*c_float),
        ('etaSine', 6*c_float),
        ('cyl', 6*c_float)
    ]

class TxHmiMru(Structure):
    _fields_ = [
        ('status', c_int),
        ('eta', 6*c_float)
    ]

class TxHmiComau(Structure):
    _fields_ = [
        ('status', c_int),
        ('q', 6*c_float),
        ('q_t', 6*c_float),
        ('qMin', 6*c_float),
        ('qMax', 6*c_float),
        ('qMax_t', 6*c_float)
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

class TxHmiWinch(Structure):
    _fields_ = [
        ('status', c_int),
        ('l', c_float)
    ]

class ST_3DMarkerPositionNoLabel(Structure):
    _fields_ = [
        ('x', c_float),
        ('y', c_float),
        ('z', c_float),
        ('id', c_int)
    ]


class TxHmiQualisys(Structure):
    _fields_ = [
        ('status', c_int),
        ('dist', c_float),
        ('x', c_float),
        ('y', c_float),
        ('z', c_float),
        ('markers', 10*ST_3DMarkerPositionNoLabel)
    ]

class TxHmi(Structure):
    _fields_ = [
        ('em8000', TxHmiStewart),
        ('em1500', TxHmiStewart),
        ('mru1', TxHmiMru),
        ('mru2', TxHmiMru),
        ('comau', TxHmiComau),
        ('winch', TxHmiWinch),
        ('qtm', TxHmiQualisys),
        ('phi', 2*c_float),
        ('phi_t', 2*c_float),
        ('e', 3*c_float),
        ('c', c_float)
    ]

class RxHmi(Structure):
    _fields_ = [
        ('counter', c_uint),
        ('winchJogUp', c_bool),
        ('winchJogDown', c_bool),
        ('xboxLeftX', c_float),
        ('xboxLeftY', c_float),
        ('xboxRightX', c_float),
        ('xboxRightY', c_float),
        ('xboxLT', c_float),
        ('xboxRT', c_float)
    ]
