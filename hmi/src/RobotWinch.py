from PyQt5 import QtCore
import numpy as np
from ctypes import Structure, sizeof
import pyads
import time
from enum import Enum

from .AdsQt import notification
from .RealTimePlot import RealTimePlot

class E_WinchMode(Enum):
    SETTLED         = 0x00
    REMOTE          = 0x01
    MOTION_COMP     = 0x02


class TxHmiWinch(Structure):
    _fields_ = [
        ('status', pyads.PLCTYPE_DINT),
        ('l', pyads.PLCTYPE_REAL)
    ]

class RobotWinch(QtCore.QObject):
    signal_eMode = QtCore.pyqtSignal(int)
    signal_bActive = QtCore.pyqtSignal(bool)

    def __init__(self, plc, gui, plcInstance, parent=None):
        super(QtCore.QObject, self).__init__(parent)
        self.plc = plc
        self.gui = gui
        self.plcInstance = plcInstance
        self.guiRoot = 'self.gui.' + self.plcInstance
        self.plcRoot = 'MAIN.' + self.plcInstance
        self.t0 = time.time()

        # Connect to gui
        eval(self.guiRoot + '_engage').clicked.connect(self.engage)
        eval(self.guiRoot + '_disengage').clicked.connect(self.disengage)

        # Connect class signals to slot
        self.signal_bActive.connect(self.slot_bActive)
        self.signal_eMode.connect(self.slot_eMode)

        # Gui singnals to slot
        eval(self.guiRoot + '_eModeCmd').currentIndexChanged.connect(self.slot_eModeCmd)

        # PLC notifications to class signals
        self.plcNotification(self.plcRoot + '.bActive', pyads.PLCTYPE_BOOL, self.signal_bActive)
        self.plcNotification(self.plcRoot + '.eMode', pyads.PLCTYPE_USINT, self.signal_eMode)

        # Init read from plc
        self.init()
        
        # Setup plot area
        self.setupPlot()

        # Plot timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)

    @QtCore.pyqtSlot(bool)
    def slot_bActive(self, value):
        if value:
            eval(self.guiRoot + '_bActive').setText('Power is ON')
        else:
            eval(self.guiRoot + '_bActive').setText('Power is OFF')

    @QtCore.pyqtSlot(int)
    def slot_eMode(self, value):
        eval(self.guiRoot + '_eMode').setText(E_WinchMode(value).name)

    @QtCore.pyqtSlot(int)
    def slot_eModeCmd(self, value):
        self.plc.write_by_name(self.plcRoot + '.eModeCmd', value, pyads.PLCTYPE_USINT)

    def update(self):
        pass

    def engage(self):
        self.plc.write_by_name(self.plcRoot + '.bEnable', True, pyads.PLCTYPE_BOOL)
    
    def disengage(self):
        self.plc.write_by_name(self.plcRoot + '.bEnable', False, pyads.PLCTYPE_BOOL)

    def setupPlot(self):
        pass

    def init(self):
        eval(self.guiRoot + '_eModeCmd').setCurrentIndex(
            self.plc.read_by_name(self.plcRoot + '.eModeCmd', pyads.PLCTYPE_USINT)
        )

    def plcNotification(self, adsName, plcType, pyqtSignal):
        # General callback function
        @notification(plcType, pyqtSignal)
        def callback(handle, name, timestamp, value):
            pass    

        attrib = pyads.NotificationAttrib(
            length=sizeof(plcType)
            # trans_mode=pyads.ADSTRANS_SERVERCYCLE,
            # max_delay=100, # Max delay in ms
            # cycle_time=500 # Cycle time in ms
        )

        # Add notification to ads
        self.plc.add_device_notification(
            adsName,
            attrib,
            callback
        )

    def close(self):
        self.timer.stop()
