from PyQt5 import QtCore, QtWidgets
from enum import Enum
from ctypes import *
import numpy as np
import pyads
import time

from .AdsQt import notification
from .RealTimePlot import RealTimePlot

MAX_STROKE = {
    'em1500': 0.4,
    'em8000': 0.8
}

class E_StewartState(Enum):
	TRANSIT 		= 0x00
	OFF				= 0x01
	SETTLED			= 0x02
	OIL_HEATING		= 0x03
	NEUTRAL 		= 0x04
	NEUTRAL_FREEZE	= 0x05
	ENGAGED			= 0x08
	ENGAGED_FREEZE	= 0x09

class E_StewartOpMode(Enum):
    MANUAL          = 0x00
    NORMAL          = 0x01

class E_StewartStatus(Enum):
    SYSTEM_OK       = 0x00
    WARNING         = 0x04
    ERROR           = 0x08

class E_StewartMode(Enum):
    SETTLED         = 0x00
    NEUTRAL         = 0x01
    SIMULATION      = 0x02
    GENERATOR       = 0x03
    REMOTE          = 0x04

class ST_TxHmiStewart(Structure):
    _fields_ = [
        ('status', pyads.PLCTYPE_UDINT),
        ('eta', pyads.PLCTYPE_ARR_REAL(6)),
        ('etaRef', pyads.PLCTYPE_ARR_REAL(6)),
        ('etaSim', pyads.PLCTYPE_ARR_REAL(6)),
        ('etaSine', pyads.PLCTYPE_ARR_REAL(6)),
        ('cyl', pyads.PLCTYPE_ARR_REAL(6))
    ]

class StewartPlattform(QtCore.QObject):
    # Async: PLC -> HMI
    signal_eMode = QtCore.pyqtSignal(int)
    signal_bError = QtCore.pyqtSignal(bool)
    signal_bReady = QtCore.pyqtSignal(bool)
    signal_bBusy = QtCore.pyqtSignal(bool)
    signal_eState = QtCore.pyqtSignal(int)
    signal_eStatus = QtCore.pyqtSignal(int)
    signal_eOpMode = QtCore.pyqtSignal(int)

    # PLC status
    eMode = E_StewartMode(0x00)
    eStatus = E_StewartStatus(0x00)

    txHmi = ST_TxHmiStewart()

    def __init__(self, plc, gui, plcInstance, parent=None):
        super(QtCore.QObject, self).__init__(parent)
        self.plc = plc
        self.gui = gui
        self.plcInstance = plcInstance
        self.guiRoot = 'self.gui.' + self.plcInstance
        self.plcRoot = 'MAIN.' + self.plcInstance
        self.t0 = time.time()
            
        # Error or warning popup box
        self.errorBox = QtWidgets.QMessageBox()
        self.errorBox.setIcon(QtWidgets.QMessageBox.Critical)
        self.errorBox.setStandardButtons(QtWidgets.QMessageBox.Reset)
        self.errorBox.buttonClicked.connect(self.slot_bReset)
        
        # Connect: ACTION -> SLOT
        eval(self.guiRoot + '_eModeCmd').currentIndexChanged.connect(self.slot_eModeCmd)
        eval(self.guiRoot + '_engage').clicked.connect(self.slot_engage)
        eval(self.guiRoot + '_disengage').clicked.connect(self.slot_disengage)

        # Connect: SIGNAL -> ACTION
        self.signal_eState.connect(self.slot_eState)
        self.signal_eStatus.connect(self.slot_eStatus)
        self.signal_eOpMode.connect(self.slot_eOpMode)
        self.signal_eMode.connect(self.slot_eMode)

        # Connect: PLC -> SIGNAL
        self.plcNotification(self.plcRoot + '.bError', pyads.PLCTYPE_BOOL, self.signal_bError)
        self.plcNotification(self.plcRoot + '.bReady', pyads.PLCTYPE_BOOL, self.signal_bReady)
        self.plcNotification(self.plcRoot + '.bBusy', pyads.PLCTYPE_BOOL, self.signal_bBusy)
        self.plcNotification(self.plcRoot + '.eState', pyads.PLCTYPE_USINT, self.signal_eState)
        self.plcNotification(self.plcRoot + '.eStatus', pyads.PLCTYPE_USINT, self.signal_eStatus)
        self.plcNotification(self.plcRoot + '.eOpMode', pyads.PLCTYPE_USINT, self.signal_eOpMode)
        self.plcNotification(self.plcRoot + '.eMode', pyads.PLCTYPE_USINT, self.signal_eMode)

        # Setup plot area
        self.setupPlot()

        # Sunchronous timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateGraph)
        self.timer.start(50)

    # QtSlots
    @QtCore.pyqtSlot(int)
    def slot_eModeCmd(self, value):
        self.plc.write_by_name(self.plcRoot + '.eModeCmd', value, pyads.PLCTYPE_SINT)

    @QtCore.pyqtSlot(int)
    def slot_eState(self, value):
        eval(self.guiRoot + '_eState').setText(E_StewartState(value).name)

    @QtCore.pyqtSlot(int)
    def slot_eStatus(self, value):
        self.eStatus = E_StewartStatus(value)
        eval(self.guiRoot + '_eStatus').setText(self.eStatus.name)

        # Warning or error popup
        if not(self.eStatus == E_StewartStatus.SYSTEM_OK):
            self.errorBox.setWindowTitle(self.eStatus.name)
            self.errorBox.setText('Click reset to return to normal operation')
            # self.errorBox.setDetailedText('Warning details goes here!')
            self.errorBox.exec_()


    @QtCore.pyqtSlot(int)
    def slot_eOpMode(self, value):
        eval(self.guiRoot + '_eOpMode').setText(E_StewartOpMode(value).name)

    @QtCore.pyqtSlot(int)
    def slot_eMode(self, value):
        self.eMode = E_StewartMode(value)
        eval(self.guiRoot + '_eMode').setText(self.eMode.name)

    @QtCore.pyqtSlot()
    def slot_bReset(self):
        self.plc.write_by_name(self.plcRoot + '.bReset', True, pyads.PLCTYPE_BOOL)

    @QtCore.pyqtSlot()
    def slot_engage(self):
        self.plc.write_by_name(self.plcRoot + '.bStart', True, pyads.PLCTYPE_BOOL)

    @QtCore.pyqtSlot()
    def slot_disengage(self):
        self.plc.write_by_name(self.plcRoot + '.bStart', False, pyads.PLCTYPE_BOOL)

    # Synchronous read function
    def updateGraph(self):
        
        self.txHmi = self.plc.read_by_name(self.plcRoot + '.txHmi', ST_TxHmiStewart)
        
        
        if self.eMode == E_StewartMode.GENERATOR:
            self.updatePlot(self.txHmi.etaSine)
        
        elif self.eMode == E_StewartMode.SIMULATION:
            self.updatePlot(self.txHmi.etaSim)

        else:
            self.updatePlot(np.zeros(6))

    def setupPlot(self):
        # UI plot instance
        plot = eval(self.guiRoot + '_plot')

        # Surge, sway and heave
        self.plotPosition = RealTimePlot(plot.addPlot())
        self.plotPosition.plot.setLabel('left', 'Position', 'm')
        self.plotPosition.plot.setYRange(-0.5, 0.5)
        self.plotPosition.add_curves(['r', 'g', 'b'], ['Surge', 'Sway', 'Heave'])

        # Roll, pitch and yaw
        plot.nextRow()
        self.plotAttitude = RealTimePlot(plot.addPlot())
        self.plotAttitude.plot.setLabel('left', 'Angle', 'deg')
        self.plotAttitude.plot.setYRange(-6.0, 6.0)
        self.plotAttitude.add_curves(['r', 'g', 'b'], ['Roll', 'Pitch', 'Yaw'])

    def updatePlot(self, eta):
        # Plot data
        t = time.time() - self.t0
        eta = np.array(eta)

        # Update plot instances
        self.plotPosition.update(t, eta[0:3])
        self.plotAttitude.update(t, eta[3:6]/np.pi*180)

        # Update stroke bars
        maxStroke = MAX_STROKE[self.plcInstance]
        eval(self.guiRoot + '_cylinder_1').setValue(self.txHmi.cyl[0]/maxStroke*100)
        eval(self.guiRoot + '_cylinder_2').setValue(self.txHmi.cyl[1]/maxStroke*100)
        eval(self.guiRoot + '_cylinder_3').setValue(self.txHmi.cyl[2]/maxStroke*100)
        eval(self.guiRoot + '_cylinder_4').setValue(self.txHmi.cyl[3]/maxStroke*100)
        eval(self.guiRoot + '_cylinder_5').setValue(self.txHmi.cyl[4]/maxStroke*100)
        eval(self.guiRoot + '_cylinder_6').setValue(self.txHmi.cyl[5]/maxStroke*100)


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

    # Function to handle the closing event of to the application
    def close(self):
        self.timer.stop()




