from ctypes import Structure, c_float, c_int, c_uint

class RemoteControlComau(Structure):
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
    
class RemoteControl(Structure):
    _fields_ = [
        ('udp_key', c_int),
        ('comau', RemoteControlComau)
    ]

class RemoteFeedbackStewart(Structure):
    _fields_ = [
        ('surge', c_float),
        ('sway', c_float),
        ('heave', c_float),
        ('roll', c_float),
        ('pitch', c_float),
        ('yaw', c_float),
        ('surge_t', c_float),
        ('sway_t', c_float),
        ('heave_t', c_float),
        ('wx', c_float),
        ('wy', c_float),
        ('wz', c_float),
        ('surge_tt', c_float),
        ('sway_tt', c_float),
        ('heave_tt', c_float),
        ('wx_t', c_float),
        ('wy_t', c_float),
        ('wz_t', c_float),
        ('L1', c_float),
        ('L2', c_float),
        ('L3', c_float),
        ('L4', c_float),
        ('L5', c_float),
        ('L6', c_float)
    ]

class RemoteFeedbackComau(Structure):
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

class RemoteFeedbackLeica(Structure):
    _fields_ = [
        ('x', c_float),
        ('y', c_float),
        ('z', c_float),
        ('q0', c_float),
        ('q1', c_float),
        ('q2', c_float),
        ('q3', c_float)
    ]

class RemoteFeedbackMru(Structure):
    _fields_ = [
        ('heave', c_float),
        ('heave_t', c_float),
        ('heave_tt', c_float),
        ('turn_rate', c_float),
        ('roll', c_float),
        ('pitch', c_float),
        ('yaw', c_float),
        ('wx', c_float),
        ('wy', c_float),
        ('wz', c_float),
        ('wx_t', c_float),
        ('wy_t', c_float),
        ('wz_t', c_float),
        ('x_t', c_float),
        ('y_t', c_float),
        ('z_t', c_float),
        ('x_tt', c_float),
        ('y_tt', c_float),
        ('z_tt', c_float)
    ]

class RemoteFeedbackShipSim(Structure):
    _fields_ = [
        ('surge', c_float),
        ('sway', c_float),
        ('heave', c_float),
        ('roll', c_float),
        ('pitch', c_float),
        ('yaw', c_float)
    ]

class RemoteFeedback(Structure):
    _fields_ = [
        ('t', c_float),
        ('em8000', RemoteFeedbackStewart),
        ('em1500', RemoteFeedbackStewart),
        ('comau', RemoteFeedbackComau),
        ('at960', RemoteFeedbackLeica),
        ('mru1', RemoteFeedbackMru),
        ('mru2', RemoteFeedbackMru),
        ('ship1', RemoteFeedbackShipSim),
        ('ship2', RemoteFeedbackShipSim)
    ]

