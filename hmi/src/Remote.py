from PyQt5 import QtCore, QtGui
import numpy as np
from ctypes import Structure, sizeof
import pyads
import time
from enum import Enum

from .AdsQt import notification
from .RealTimePlot import RealTimePlot

from .MotionLab import MotionLab

# class Remote(QtCore.QObject):
class Remote(MotionLab):
    signal_bActive = QtCore.pyqtSignal(bool)

    def __init__(self, plc, gui, plcInstance, parent=None):
        # super(QtCore.QObject, self).__init__(parent)
        super(MotionLab, self).__init__(parent)
        self.plc = plc
        self.gui = gui
        self.plcInstance = plcInstance
        self.guiRoot = 'self.gui.' + self.plcInstance
        self.plcRoot = 'MAIN.' + self.plcInstance
        self.t0 = time.time()

        # GUI -> SLOT
        
        # PLC -> SIGNAL
        self.plcNotification(self.plcRoot + '.bActive', pyads.PLCTYPE_BOOL, self.signal_bActive)
        
        # SIGNAL -> SLOT
        self.signal_bActive.connect(self.slot_bActive)

        # Initial LED state
        eval(self.guiRoot + '_bActive').setPixmap(QtGui.QPixmap('./icons/led-off.png'))
        eval(self.guiRoot + '_bActive').setScaledContents(True)


        # Plot timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)

    @QtCore.pyqtSlot(bool)
    def slot_bActive(self, value):
        if value:
            eval(self.guiRoot + '_bActive').setPixmap(QtGui.QPixmap('./icons/led-on.png'))

        
        else:
            eval(self.guiRoot + '_bActive').setPixmap(QtGui.QPixmap('./icons/led-off.png'))
    
    def update(self):
        pass
    
    def close(self):
        self.timer.stop()
