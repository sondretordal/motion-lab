from PyQt5 import QtCore, QtWidgets, QtGui
from enum import Enum
from ctypes import Structure, sizeof
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
        ('cyl', pyads.PLCTYPE_ARR_REAL(6)),
        ('dofScale', pyads.PLCTYPE_ARR_REAL(6))
    ]

class StewartPlattform(QtCore.QObject):
    # Async: PLC -> HMI
    signal_eMode = QtCore.pyqtSignal(int)
    signal_bError = QtCore.pyqtSignal(bool)
    signal_bActive = QtCore.pyqtSignal(bool)
    signal_bBusy = QtCore.pyqtSignal(bool)
    signal_eState = QtCore.pyqtSignal(int)
    signal_eStatus = QtCore.pyqtSignal(int)
    signal_eOpMode = QtCore.pyqtSignal(int)

    # PLC status
    eState = E_StewartState(0x00)
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
        self.signal_bActive.connect(self.slot_bActive)

        # Connect: PLC -> SIGNAL
        self.plcNotification(self.plcRoot + '.bError', pyads.PLCTYPE_BOOL, self.signal_bError)
        self.plcNotification(self.plcRoot + '.bActive', pyads.PLCTYPE_BOOL, self.signal_bActive)
        self.plcNotification(self.plcRoot + '.bBusy', pyads.PLCTYPE_BOOL, self.signal_bBusy)
        self.plcNotification(self.plcRoot + '.eState', pyads.PLCTYPE_USINT, self.signal_eState)
        self.plcNotification(self.plcRoot + '.eStatus', pyads.PLCTYPE_USINT, self.signal_eStatus)
        self.plcNotification(self.plcRoot + '.eOpMode', pyads.PLCTYPE_USINT, self.signal_eOpMode)
        self.plcNotification(self.plcRoot + '.eMode', pyads.PLCTYPE_USINT, self.signal_eMode)

        # Set intial avtivity LED status
        eval(self.guiRoot + '_bActive').setScaledContents(True)

        
        # Setup plot area
        self.setupPlot()

        # Setup sine wave input fields
        self.intilizeHmiFields()
        self.setupSineWaveInputs()
        self.connectSineWaveInputs()

        # Deactivate sine inputs on startup
        self.disableSineInputs()
        
        # Timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)

    # QtSlots
    @QtCore.pyqtSlot(int)
    def slot_eModeCmd(self, value):
        self.plc.write_by_name(self.plcRoot + '.eModeCmd', value, pyads.PLCTYPE_SINT)

    @QtCore.pyqtSlot(int)
    def slot_eState(self, value):
        self.eState = E_StewartState(value)
        eval(self.guiRoot + '_eState').setText(E_StewartState(value).name)

    @QtCore.pyqtSlot(int)
    def slot_eStatus(self, value):
        self.eStatus = E_StewartStatus(value)
        eval(self.guiRoot + '_eStatus').setText(self.eStatus.name)

        # Warning or error popup
        if not (self.eStatus == E_StewartStatus.SYSTEM_OK):
            self.errorBox.setWindowTitle(
                self.plcInstance + ': ' + self.eStatus.name
            )
            self.errorBox.setText('Click reset to return to normal operation')
            # self.errorBox.setDetailedText('Warning details goes here!')
            self.errorBox.exec_()

    @QtCore.pyqtSlot(int)
    def slot_eOpMode(self, value):
        eval(self.guiRoot + '_eOpMode').setText(E_StewartOpMode(value).name)

    @QtCore.pyqtSlot(int)
    def slot_eMode(self, value):
        self.eMode = E_StewartMode(value)
        self.enableSineInputs()
        eval(self.guiRoot + '_eMode').setText(self.eMode.name)

    @QtCore.pyqtSlot()
    def slot_bReset(self):
        eval(self.guiRoot + '_eModeCmd').setCurrentIndex(0)
        self.plc.write_by_name(self.plcRoot + '.bReset', True, pyads.PLCTYPE_BOOL)

    @QtCore.pyqtSlot()
    def slot_engage(self):
        self.plc.write_by_name(self.plcRoot + '.bStart', True, pyads.PLCTYPE_BOOL)

        if self.eMode == E_StewartMode.GENERATOR:
            self.disableSineInputs()

    @QtCore.pyqtSlot()
    def slot_disengage(self):
        self.plc.write_by_name(self.plcRoot + '.bStart', False, pyads.PLCTYPE_BOOL)

        if self.eMode == E_StewartMode.GENERATOR:
            self.enableSineInputs()

    @QtCore.pyqtSlot(bool)
    def slot_bActive(self, value):
        if value:
            eval(self.guiRoot + '_bActive').setPixmap(QtGui.QPixmap('./icons/led-on.png'))

        else:
            eval(self.guiRoot + '_bActive').setPixmap(QtGui.QPixmap('./icons/led-off.png'))


    def intilizeHmiFields(self):
        # Read data from PLC to intilize the HMI fields
        eval(self.guiRoot + '_eModeCmd').setCurrentIndex(
            self.plc.read_by_name(self.plcRoot + '.eModeCmd', pyads.PLCTYPE_USINT)
        )

        # Read amplitude, frequency and phase settings from PLC
        for i in range(0, 6):
            amp = eval(self.guiRoot + '_amp_' + str(i))
            freq = eval(self.guiRoot + '_freq_' + str(i))
            phase = eval(self.guiRoot + '_phase_' + str(i))

            if i < 3:
                amp.setValue(
                    self.plc.read_by_name(self.plcRoot + '.sineAmplitude[' + str(i) + ']', pyads.PLCTYPE_LREAL)
                )

            else:
                amp.setValue(
                    self.plc.read_by_name(self.plcRoot + '.sineAmplitude[' + str(i) + ']', pyads.PLCTYPE_LREAL)/np.pi*180
                )

            freq.setValue(
                self.plc.read_by_name(self.plcRoot + '.sineOmega[' + str(i) + ']', pyads.PLCTYPE_LREAL)/(2*np.pi)
            )

            phase.setValue(
                self.plc.read_by_name(self.plcRoot + '.sinePhase[' + str(i) + ']', pyads.PLCTYPE_LREAL)/np.pi*180
            )

            # Read max DOF settings from PLC
            self.etaRefMin = self.plc.read_by_name(
                self.plcRoot + '.etaRefMin', pyads.PLCTYPE_ARR_LREAL(6)
            )

            self.etaRefMax = self.plc.read_by_name(
                self.plcRoot + '.etaRefMax', pyads.PLCTYPE_ARR_LREAL(6)
            )

    def disableSineInputs(self):    
        for i in range(0, 6):
            eval(self.guiRoot + '_amp_' + str(i)).setDisabled(True)
            eval(self.guiRoot + '_freq_' + str(i)).setDisabled(True)
            eval(self.guiRoot + '_phase_' + str(i)).setDisabled(True)

    def enableSineInputs(self):    
        for i in range(0, 6):
            eval(self.guiRoot + '_amp_' + str(i)).setDisabled(False)
            eval(self.guiRoot + '_freq_' + str(i)).setDisabled(False)
            eval(self.guiRoot + '_phase_' + str(i)).setDisabled(False)

    def update(self):
        # Read HMI data bundle
        self.txHmi = self.plc.read_by_name(self.plcRoot + '.txHmi', ST_TxHmiStewart)

        # Plot
        if self.txHmi.status != 0:
            if self.eState == E_StewartState.ENGAGED:
                # Plot feedback when engaged
                self.updatePlot(self.txHmi.eta)

            else:
                # Plot input reference when else
                self.updatePlot(self.txHmi.etaRef)

        # TODO: Mowe into wave simualtor
        # Plot Hydro Simualator scaling
        for i in range(0, 5):
            eval(self.guiRoot + '_dof_scale_' + str(i)).setValue(int(self.txHmi.dofScale[i]*100))

    def setupPlot(self):
        # Surge, sway and heave
        self.plotPosition = RealTimePlot(eval(self.guiRoot + '_plot').addPlot())
        self.plotPosition.plot.setLabel('left', 'Position', 'm')
        self.plotPosition.plot.setYRange(-0.5, 0.5)
        self.plotPosition.add_curves(['r', 'g', 'b'], ['Surge', 'Sway', 'Heave'])

        # Roll, pitch and yaw
        eval(self.guiRoot + '_plot').nextRow()
        self.plotAttitude = RealTimePlot(eval(self.guiRoot + '_plot').addPlot())
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

    def connectSineWaveInputs(self):
        # Connect sine wave paramters to PLC
        eval(self.guiRoot + '_amp_0').valueChanged.connect(lambda:
            self.plc.write_by_name(self.plcRoot + '.sineAmplitude[0]', eval(self.guiRoot + '_amp_0').value(), pyads.PLCTYPE_LREAL)
        )

        eval(self.guiRoot + '_amp_1').valueChanged.connect(lambda:
            self.plc.write_by_name(self.plcRoot + '.sineAmplitude[1]', eval(self.guiRoot + '_amp_1').value(), pyads.PLCTYPE_LREAL)
        )

        eval(self.guiRoot + '_amp_2').valueChanged.connect(lambda:
            self.plc.write_by_name(self.plcRoot + '.sineAmplitude[2]', eval(self.guiRoot + '_amp_2').value(), pyads.PLCTYPE_LREAL)
        )

        eval(self.guiRoot + '_amp_3').valueChanged.connect(lambda:
            self.plc.write_by_name(self.plcRoot + '.sineAmplitude[3]', eval(self.guiRoot + '_amp_3').value()/180*np.pi, pyads.PLCTYPE_LREAL)
        )
        
        eval(self.guiRoot + '_amp_4').valueChanged.connect(lambda:
            self.plc.write_by_name(self.plcRoot + '.sineAmplitude[4]', eval(self.guiRoot + '_amp_4').value()/180*np.pi, pyads.PLCTYPE_LREAL)
        )
        
        eval(self.guiRoot + '_amp_5').valueChanged.connect(lambda:
            self.plc.write_by_name(self.plcRoot + '.sineAmplitude[5]', eval(self.guiRoot + '_amp_5').value()/180*np.pi, pyads.PLCTYPE_LREAL)
        )

        eval(self.guiRoot + '_freq_0').valueChanged.connect(lambda:
            self.plc.write_by_name(self.plcRoot + '.sineOmega[0]', eval(self.guiRoot + '_freq_0').value()*2*np.pi, pyads.PLCTYPE_LREAL)
        )

        eval(self.guiRoot + '_freq_1').valueChanged.connect(lambda:
            self.plc.write_by_name(self.plcRoot + '.sineOmega[1]', eval(self.guiRoot + '_freq_1').value()*2*np.pi, pyads.PLCTYPE_LREAL)
        )

        eval(self.guiRoot + '_freq_2').valueChanged.connect(lambda:
            self.plc.write_by_name(self.plcRoot + '.sineOmega[2]', eval(self.guiRoot + '_freq_2').value()*2*np.pi, pyads.PLCTYPE_LREAL)
        )

        eval(self.guiRoot + '_freq_3').valueChanged.connect(lambda:
            self.plc.write_by_name(self.plcRoot + '.sineOmega[3]', eval(self.guiRoot + '_freq_3').value()*2*np.pi, pyads.PLCTYPE_LREAL)
        )

        eval(self.guiRoot + '_freq_4').valueChanged.connect(lambda:
            self.plc.write_by_name(self.plcRoot + '.sineOmega[4]', eval(self.guiRoot + '_freq_4').value()*2*np.pi, pyads.PLCTYPE_LREAL)
        )

        eval(self.guiRoot + '_freq_5').valueChanged.connect(lambda:
            self.plc.write_by_name(self.plcRoot + '.sineOmega[5]', eval(self.guiRoot + '_freq_5').value()*2*np.pi, pyads.PLCTYPE_LREAL)
        )

        eval(self.guiRoot + '_phase_0').valueChanged.connect(lambda:
            self.plc.write_by_name(self.plcRoot + '.sinePhase[0]', eval(self.guiRoot + '_phase_0').value()/180*np.pi, pyads.PLCTYPE_LREAL)
        )

        eval(self.guiRoot + '_phase_1').valueChanged.connect(lambda:
            self.plc.write_by_name(self.plcRoot + '.sinePhase[1]', eval(self.guiRoot + '_phase_1').value()/180*np.pi, pyads.PLCTYPE_LREAL)
        )

        eval(self.guiRoot + '_phase_2').valueChanged.connect(lambda:
            self.plc.write_by_name(self.plcRoot + '.sinePhase[2]', eval(self.guiRoot + '_phase_2').value()/180*np.pi, pyads.PLCTYPE_LREAL)
        )

        eval(self.guiRoot + '_phase_3').valueChanged.connect(lambda:
            self.plc.write_by_name(self.plcRoot + '.sinePhase[3]', eval(self.guiRoot + '_phase_3').value()/180*np.pi, pyads.PLCTYPE_LREAL)
        )

        eval(self.guiRoot + '_phase_4').valueChanged.connect(lambda:
            self.plc.write_by_name(self.plcRoot + '.sinePhase[4]', eval(self.guiRoot + '_phase_4').value()/180*np.pi, pyads.PLCTYPE_LREAL)
        )

        eval(self.guiRoot + '_phase_5').valueChanged.connect(lambda:
            self.plc.write_by_name(self.plcRoot + '.sinePhase[5]', eval(self.guiRoot + '_phase_5').value()/180*np.pi, pyads.PLCTYPE_LREAL)
        )

    def setupSineWaveInputs(self):
        # Setup sine wave input fields
        for i in range(0, 6):
            amp = eval(self.guiRoot + '_amp_' + str(i))
            freq = eval(self.guiRoot + '_freq_' + str(i))
            phase = eval(self.guiRoot + '_phase_' + str(i))

            # Amplitude settings
            if i < 3:
                # Position
                amp.setDecimals(2)
                amp.setSingleStep(0.01)
                amp.setMinimum(self.etaRefMin[i])
                amp.setMaximum(self.etaRefMax[i])

            else:
                # Attitude
                amp.setDecimals(1)
                amp.setSingleStep(0.1)
                amp.setMinimum(self.etaRefMin[i]/np.pi*180)
                amp.setMaximum(self.etaRefMax[i]/np.pi*180)
            
            # Frequency settings
            freq.setDecimals(2)
            freq.setSingleStep(0.02)
            freq.setMinimum(0.01)
            freq.setMaximum(1.0)

            # Phase settings
            phase.setDecimals(1)
            phase.setSingleStep(10)
            phase.setMinimum(-180)
            phase.setMaximum(180)

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




