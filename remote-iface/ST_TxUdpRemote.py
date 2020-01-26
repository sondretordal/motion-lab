import ctypes

class ST_TxUdpRemote(ctypes.Structure):
    _fields_ = [
        ('eMode', ctypes.c_uint32),
        ('t', ctypes.c_float),

        ('comau_q', ctypes.c_float*6),
        ('comau_q_t', ctypes.c_float*6),

        ('winch_l', ctypes.c_float),
        ('winch_l_t', ctypes.c_float),

        ('em8000_eta', ctypes.c_float*6),
        ('em8000_eta_t', ctypes.c_float*6),
        ('em8000_eta_tt', ctypes.c_float*6),

        ('mru1_eta', ctypes.c_float*6),
        ('mru1_v', ctypes.c_float*6),

        ('em1500_eta', ctypes.c_float*6),
        ('em1500_eta_t', ctypes.c_float*6),
        ('em1500_eta_tt', ctypes.c_float*6),

        ('mru2_eta', ctypes.c_float*6),
        ('mru2_v', ctypes.c_float*6)
    ]





