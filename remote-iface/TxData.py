from ctypes import Structure
import pyads

class TxData(Structure):
    _fields_ = [
        ('eModeCmd', pyads.PLCTYPE_UDINT),

        ('comau_u', pyads.PLCTYPE_ARR_REAL(6)),
        ('winch_u', pyads.PLCTYPE_REAL)
        
    ]





