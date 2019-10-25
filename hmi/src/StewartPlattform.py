from PyQt5 import QtCore
from enum import Enum
from ctypes import sizeof
import numpy as np
import pyads
import time

from .AdsQt import notification

class E_StewartState(Enum):
    TRANSIT = 0
    OFF = 1
    SETTLED = 2
    OIL_HEATING = 3
    NEUTRAL = 4
    NEUTRAL_FREEZE = 5
    ENGAGED = 6
    ENGAGED_FREEZE = 7

class E_StewartOpMode(Enum):
    MANUAL = 0
    NORMAL = 1

class E_StewartStatus(Enum):
    SYSTEM_OK = 0
    WARNING = 1
    ERROR = 2

class E_StewartMode(Enum):
    SETTLED = 0
    NEUTRAL = 1
    SIMULATION = 2
    GENERATOR = 3
    REMOTE = 4


class StewartPlattform(QtCore.QObject):
    # Async: HMI -> PLC
    eModeCmd = QtCore.pyqtSignal(int)
    
    # Async: PLC -> HMI
    bError = QtCore.pyqtSignal(bool)
    bReady = QtCore.pyqtSignal(bool)
    bBusy = QtCore.pyqtSignal(bool)
    eState = QtCore.pyqtSignal(int)
    eStatus = QtCore.pyqtSignal(int)
    eOpMode = QtCore.pyqtSignal(int)

    # Sync: PLC -> HMI
    eta = np.zeros(6)
    eta_t = np.zeros(6)
    eta_tt = np.zeros(6)

    def __init__(self, plc, gui, plcInstance, parent=None):
        super(QtCore.QObject, self).__init__(parent)
        self.plc = plc
        self.gui = gui
        self.guiRoot = 'self.gui.' + plcInstance
        self.plcRoot = 'MAIN.' + plcInstance

        # Connect: ACTION -> SIGNAL
        eval(self.guiRoot + '_eModeCmd').currentIndexChanged.connect(self.eModeCmd)

        # Connect: SIGNAL -> PLC
        self.eModeCmd.connect(self.write_eModeCmd)

        # Connect: SIGNAL -> ACTION
        self.bBusy.connect(self.test)
        self.eState.connect(self.action_eState)
        self.eStatus.connect(self.action_eStatus)
        self.eOpMode.connect(self.action_eOpMode)

        # Connect: PLC -> SIGNAL
        self.plcNotification(self.plcRoot + '.bError', pyads.PLCTYPE_BOOL, self.bError)
        self.plcNotification(self.plcRoot + '.bReady', pyads.PLCTYPE_BOOL, self.bReady)
        self.plcNotification(self.plcRoot + '.bBusy', pyads.PLCTYPE_BOOL, self.bBusy)
        self.plcNotification(self.plcRoot + '.eState', pyads.PLCTYPE_USINT, self.eState)
        self.plcNotification(self.plcRoot + '.eStatus', pyads.PLCTYPE_USINT, self.eStatus)
        self.plcNotification(self.plcRoot + '.eOpMode', pyads.PLCTYPE_USINT, self.eOpMode)

        



    # Write to PLC
    @QtCore.pyqtSlot(int)
    def write_eModeCmd(self, value):
        self.plc.write_by_name(self.plcRoot + '.eModeCmd', value, pyads.PLCTYPE_SINT)

    @QtCore.pyqtSlot(bool)
    def test(self, value):
        print('EM1500' + str(value))

    # On PLC notification actions
    @QtCore.pyqtSlot(int)
    def action_eState(self, value):
        eval(self.guiRoot + '_eState').setText(E_StewartState(value).name)

    @QtCore.pyqtSlot(int)
    def action_eStatus(self, value):
        eval(self.guiRoot + '_eStatus').setText(E_StewartStatus(value).name)
        print(value)

    @QtCore.pyqtSlot(int)
    def action_eOpMode(self, value):
        eval(self.guiRoot + '_eOpMode').setText(E_StewartOpMode(value).name)    

    # Helper functions
    def plcNotification(self, adsName, plcType, pyqtSignal):

        # # Initial read
        # value = self.plc.read_by_name(adsName, plcType)
        # pyqtSignal.emit(value)
        # print(adsName + ' = ' + str(value))

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




