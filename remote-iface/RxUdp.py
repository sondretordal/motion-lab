import ctypes

class RxUdp(ctypes.Structure):
    _fields_ = [
        # Current operation mode and PLC time [s]
        ('eMode', ctypes.c_uint32),
        ('t', ctypes.c_float),
        
        # Comau angle feedback in [rad]
        ('comau_q1', ctypes.c_float),
        ('comau_q2', ctypes.c_float),
        ('comau_q3', ctypes.c_float),
        ('comau_q4', ctypes.c_float),
        ('comau_q5', ctypes.c_float),
        ('comau_q6', ctypes.c_float),

        # Comau angular speed feedback in [rad/s]
        ('comau_q1_t', ctypes.c_float),
        ('comau_q2_t', ctypes.c_float),
        ('comau_q3_t', ctypes.c_float),
        ('comau_q4_t', ctypes.c_float),
        ('comau_q5_t', ctypes.c_float),
        ('comau_q6_t', ctypes.c_float),

        # Winch wire length in [m] and speed in [m/s]
        ('winch_l', ctypes.c_float),
        ('winch_l_t', ctypes.c_float),

        # EM8000 translational positions in [m]
        ('em8000_surge', ctypes.c_float),
        ('em8000_sway', ctypes.c_float),
        ('em8000_heave', ctypes.c_float),

        # EM8000 euler angles in [rad]
        ('em8000_roll', ctypes.c_float),
        ('em8000_pitch', ctypes.c_float),
        ('em8000_yaw', ctypes.c_float),

        # EM8000 translational velocites in [m/s]
        ('em8000_surge_t', ctypes.c_float),
        ('em8000_sway_t', ctypes.c_float),
        ('em8000_heave_t', ctypes.c_float),

        # EM8000 euler velocites in [rad/s]
        ('em8000_roll_t', ctypes.c_float),
        ('em8000_pitch_t', ctypes.c_float),
        ('em8000_yaw_t', ctypes.c_float),

        # EM8000 translational accelerations in [m/s^2]
        ('em8000_surge_tt', ctypes.c_float),
        ('em8000_sway_tt', ctypes.c_float),
        ('em8000_heave_tt', ctypes.c_float),

        # EM8000 euler accelerations in [rad/s^2]
        ('em8000_roll_tt', ctypes.c_float),
        ('em8000_pitch_tt', ctypes.c_float),
        ('em8000_yaw_tt', ctypes.c_float),

        # MRU1 (EM8000) translational positions in [m]
        ('mru1_surge', ctypes.c_float),
        ('mru1_sway', ctypes.c_float),
        ('mru1_heave', ctypes.c_float),

        # MRU1 (EM8000) euler angles in [rad]
        ('mru1_roll', ctypes.c_float),
        ('mru1_pitch', ctypes.c_float),
        ('mru1_yaw', ctypes.c_float),

        # MRU1 (EM8000) translational velocites in [m/s]
        ('mru1_surge_t', ctypes.c_float),
        ('mru1_sway_t', ctypes.c_float),
        ('mru1_heave_t', ctypes.c_float),

        # MRU1 (EM8000) body velocities in [rad/s]
        ('mru1_wx', ctypes.c_float),
        ('mru1_wy', ctypes.c_float),
        ('mru1_wz', ctypes.c_float),

        # EM1500 translational positions in [m]
        ('em1500_surge', ctypes.c_float),
        ('em1500_sway', ctypes.c_float),
        ('em1500_heave', ctypes.c_float),

        # EM1500 euler angles in [rad]
        ('em1500_roll', ctypes.c_float),
        ('em1500_pitch', ctypes.c_float),
        ('em1500_yaw', ctypes.c_float),

        # EM1500 translational velocites in [m/s]
        ('em1500_surge_t', ctypes.c_float),
        ('em1500_sway_t', ctypes.c_float),
        ('em1500_heave_t', ctypes.c_float),

        # EM1500 euler velocites in [rad/s]
        ('em1500_roll_t', ctypes.c_float),
        ('em1500_pitch_t', ctypes.c_float),
        ('em1500_yaw_t', ctypes.c_float),

        # EM1500 translational accelerations in [m/s^2]
        ('em1500_surge_tt', ctypes.c_float),
        ('em1500_sway_tt', ctypes.c_float),
        ('em1500_heave_tt', ctypes.c_float),

        # EM1500 euler accelerations in [rad/s^2]
        ('em1500_roll_tt', ctypes.c_float),
        ('em1500_pitch_tt', ctypes.c_float),
        ('em1500_yaw_tt', ctypes.c_float),

        # MRU1 (EM1500) translational positions in [m]
        ('mru1_surge', ctypes.c_float),
        ('mru1_sway', ctypes.c_float),
        ('mru1_heave', ctypes.c_float),

        # MRU1 (EM1500) euler angles in [rad]
        ('mru1_roll', ctypes.c_float),
        ('mru1_pitch', ctypes.c_float),
        ('mru1_yaw', ctypes.c_float),

        # MRU1 (EM1500) translational velocites in [m/s]
        ('mru1_surge_t', ctypes.c_float),
        ('mru1_sway_t', ctypes.c_float),
        ('mru1_heave_t', ctypes.c_float),

        # MRU1 (EM1500) body velocities in [rad/s]
        ('mru1_wx', ctypes.c_float),
        ('mru1_wy', ctypes.c_float),
        ('mru1_wz', ctypes.c_float)
    ]