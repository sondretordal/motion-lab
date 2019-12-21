from PyQt5 import QtCore, QtGui
import numpy as np
from ctypes import Structure, sizeof
import pyads
import time
from enum import Enum

from .AdsQt import notification
from .RealTimePlot import RealTimePlot


class TxHmiComau(Structure):
    _fields_ = [
        ('status', pyads.PLCTYPE_DINT),
        ('u', pyads.PLCTYPE_ARR_REAL(6)),
        ('q', pyads.PLCTYPE_ARR_REAL(6)),
        ('q_t', pyads.PLCTYPE_ARR_REAL(6)),
        ('qMin', pyads.PLCTYPE_ARR_REAL(6)),
        ('qMax', pyads.PLCTYPE_ARR_REAL(6)),
        ('qMax_t', pyads.PLCTYPE_ARR_REAL(6))
    ]

class TxHmiWinch(Structure):
    _fields_ = [
        ('status', pyads.PLCTYPE_DINT),
        ('l', pyads.PLCTYPE_REAL)
    ]

class ComauRobot(QtCore.QObject):
    signal_bActive = QtCore.pyqtSignal(bool)

    def __init__(self, plc, gui, plcInstance, parent=None):
        super(QtCore.QObject, self).__init__(parent)
        self.plc = plc
        self.gui = gui
        self.plcInstance = plcInstance
        self.guiRoot = 'self.gui.' + self.plcInstance
        self.plcRoot = 'MAIN.' + self.plcInstance
        self.t0 = time.time()

        # Setup plot area
        self.setupPlot()
        
        # GUI -> SLOT
        self.gui.comau_engage.clicked.connect(self.engage)
        self.gui.comau_disengage.clicked.connect(self.disengage)

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
        self.txHmi = self.plc.read_by_name(
            'MAIN.comau.txHmi',
            TxHmiComau
        )

        # Plot
        t = time.time() - self.t0
        self.plotInput.update(t, np.array(self.txHmi.u)/np.pi*180)
        self.plotAngles.update(t, np.array(self.txHmi.q)/np.pi*180)

        # Bars
        q = self.txHmi.q
        qMin = self.txHmi.qMin
        qMax = self.txHmi.qMax
        for i in range(0, 6):
            # Robot Stroke utilization
            A = qMax[i] - qMin[i]
            if A != 0.0:
                stroke = (q[i] - qMin[i])/A*100
                if stroke < 50:
                    stroke = np.floor(stroke)
                else:
                    stroke = np.ceil(stroke)

                eval('self.gui.comau_q_' + str(i)).setValue(stroke)

    def engage(self):
        self.plc.write_by_name('MAIN.comau.bStart', True, pyads.PLCTYPE_BOOL)
    
    def disengage(self):
        self.plc.write_by_name('MAIN.comau.bStart', False, pyads.PLCTYPE_BOOL)

    def setupPlot(self):
        self.plotInput = RealTimePlot(self.gui.comau_plot.addPlot())
        self.plotInput.plot.setLabel('left', 'Input', 'deg/s')
        self.plotInput.plot.setYRange(-10, 10)
        self.plotInput.add_curves(
            ['b', 'g', 'r', 'c', 'm', 'y'],
            ['u1', 'u2', 'u3', 'u4', 'u5', 'u6']
        )

        self.gui.comau_plot.nextRow()
        self.plotAngles = RealTimePlot(self.gui.comau_plot.addPlot())
        self.plotAngles.plot.setLabel('left', 'Angles', 'deg')
        self.plotAngles.plot.setYRange(-120, 90)
        self.plotAngles.add_curves(
            ['b', 'g', 'r', 'c', 'm', 'y'],
            ['q1', 'q2', 'q3', 'q4', 'q5', 'q6']
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
