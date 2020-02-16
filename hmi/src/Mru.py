from PyQt5 import QtCore, QtGui
import numpy as np
from ctypes import sizeof
import pyads
import time
from enum import Enum

from .AdsQt import notification
from .RealTimePlot import RealTimePlot

class Mru(QtCore.QObject):
    signal_bActive = QtCore.pyqtSignal(bool)

    def __init__(self, plc, gui, plcInstance, parent=None):
        super(QtCore.QObject, self).__init__(parent)
        self.plc = plc
        self.gui = gui
        self.plcInstance = plcInstance
        self.guiRoot = 'self.gui.' + self.plcInstance
        self.plcRoot = 'MAIN.' + self.plcInstance

        # PLC -> Signal
        self.plcNotification(self.plcRoot + '.bActive', pyads.PLCTYPE_BOOL, self.signal_bActive)

        # SIGNAL -> SLOT
        self.signal_bActive.connect(self.slot_bActive)

        # Set intial led status
        eval(self.guiRoot + '_bActive').setPixmap(QtGui.QPixmap('./icons/led-off.png'))
        eval(self.guiRoot + '_bActive').setScaledContents(True)


    @QtCore.pyqtSlot(bool)
    def slot_bActive(self, value):
        if value:
            eval(self.guiRoot + '_bActive').setPixmap(QtGui.QPixmap('./icons/led-on.png'))

        else:
            eval(self.guiRoot + '_bActive').setPixmap(QtGui.QPixmap('./icons/led-off.png'))

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
        pass
