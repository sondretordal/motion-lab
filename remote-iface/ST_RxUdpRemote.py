import ctypes

class ST_RxUdpRemote(ctypes.Structure):
    _fields_ = [
        ('iCounter', ctypes.c_uint32),
        ('eModeCmd', ctypes.c_uint32),

        ('em8000_u', ctypes.c_float*6),
        ('em1500_u', ctypes.c_float*6),
        ('comau_u', ctypes.c_float*6),
        ('winch_u', ctypes.c_float)
        
    ]





