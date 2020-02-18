import ctypes

class TxUdp(ctypes.Structure):
    _fields_ = [
        # Activity counter
        ('iCounter', ctypes.c_uint32),

        # Mode command (inactive as for now....)
        ('eModeCmd', ctypes.c_uint32),

        # EM8000 position commands in [m]
        ('em8000_surge_cmd', ctypes.c_float),
        ('em8000_sway_cmd', ctypes.c_float),
        ('em8000_heave_cmd', ctypes.c_float),

        # EM8000 euler angle commands in [rad]
        ('em8000_roll_cmd', ctypes.c_float),
        ('em8000_pitch_cmd', ctypes.c_float),
        ('em8000_yaw_cmd', ctypes.c_float),

        # EM8000 position commands in [m]
        ('em1500_surge_cmd', ctypes.c_float),
        ('em1500_sway_cmd', ctypes.c_float),
        ('em1500_heave_cmd', ctypes.c_float),

        # EM1500 euler angle commands in [rad]
        ('em1500_roll_cmd', ctypes.c_float),
        ('em1500_pitch_cmd', ctypes.c_float),
        ('em1500_yaw_cmd', ctypes.c_float),

        # Comau robot joint speed commands in [rad/s]
        ('comau_q1_t_cmd', ctypes.c_float),
        ('comau_q2_t_cmd', ctypes.c_float),
        ('comau_q3_t_cmd', ctypes.c_float),
        ('comau_q4_t_cmd', ctypes.c_float),
        ('comau_q5_t_cmd', ctypes.c_float),
        ('comau_q6_t_cmd', ctypes.c_float),

        # Winch speed command in [m/s]
        ('winch_l_t_cmd', ctypes.c_float)
    ]