from PyQt5 import QtCore
import numpy as np
from ctypes import Structure
import pyads
import time

class TxHmiComau(Structure):
    _fields_ = [
        ('status', pyads.PLCTYPE_DINT),
        ('q', pyads.PLCTYPE_ARR_REAL(6)),
        ('q_t', pyads.PLCTYPE_ARR_REAL(6)),
        ('qMin', pyads.PLCTYPE_ARR_REAL(6)),
        ('qMax', pyads.PLCTYPE_ARR_REAL(6)),
        ('qMax_t', pyads.PLCTYPE_ARR_REAL(6))
    ]

class ComauRobot(QtCore.QObject):
    def __init__(self, plc, gui, plcInstance, parent=None):
        super(QtCore.QObject, self).__init__(parent)
        self.plc = plc
        self.gui = gui
        self.plcInstance = plcInstance
        self.guiRoot = 'self.gui.' + self.plcInstance
        self.plcRoot = 'MAIN.' + self.plcInstance
        self.t0 = time.time()