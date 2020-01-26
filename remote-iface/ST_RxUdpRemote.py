from ctypes import Structure
import pyads

class ST_RxUdpRemote(Structure):
    _fields_ = [
        ('iCounter', pyads.PLCTYPE_UDINT),
        ('eModeCmd', pyads.PLCTYPE_UDINT),

        ('em8000_u', pyads.PLCTYPE_ARR_REAL(6)),
        ('em1500_u', pyads.PLCTYPE_ARR_REAL(6)),
        ('comau_u', pyads.PLCTYPE_ARR_REAL(6)),
        ('winch_u', pyads.PLCTYPE_REAL)
        
    ]





