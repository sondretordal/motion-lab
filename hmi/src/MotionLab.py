from PyQt5 import QtWidgets, QtCore, QtGui
import pyqtgraph as pg
import pyads
import json
from ctypes import sizeof
from datetime import datetime
from enum import Enum

# TODO: Implement this
from src.opengl import MotionLabVisualizer

# NEW
from .AdsQt import notification
from .MainWindow import Ui_MainWindow
from .StewartPlattform import StewartPlattform
from .ComauRobot import ComauRobot
from .RobotWinch import RobotWinch
from .WaveSimulator import WaveSimulator
from .DataLogger import DataLogger
# from .Remote import Remote
from .Mru import Mru
from .Qtm import Qtm


# Motionlab pybind module
from lib import motionlab as ml

# Background color pyqtgraph
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
pg.setConfigOptions(antialias=True)


class E_MotionLabState(Enum):
    STOP 		= 0x00
    NORMAL      = 0x01
    ERROR		= 0x10

class MotionLab(QtWidgets.QMainWindow, Ui_MainWindow):
    signal_logMessage = QtCore.pyqtSignal(str)
    signal_eState = QtCore.pyqtSignal(int)

    def __init__(self):
        super(MotionLab, self).__init__()
        self.gui = Ui_MainWindow()
        self.gui.setupUi(self)

        # Set size to fixed
        self.setFixedSize(self.size())

        # Start ADS communications
        self.plc = pyads.Connection('192.168.90.150.1.1', 851)
        self.plc.open()

        try:
            self.plc.read_state()
            self.plcActive = True

        except pyads.ADSError:
            self.plcActive = False
        
        # Connect UI
        if self.plcActive:
            # Physical equipement
            self.em1500 = StewartPlattform(self.plc, self.gui, 'em1500')
            self.em8000 = StewartPlattform(self.plc, self.gui, 'em8000')
            self.comau = ComauRobot(self.plc, self.gui, 'comau')
            self.winch = RobotWinch(self.plc, self.gui, 'winch')
            self.mru1 = Mru(self.plc, self.gui, 'mru1')
            self.mru2 = Mru(self.plc, self.gui, 'mru2')
            # self.remote = Remote(self.plc, self.gui, 'remote', self)
            self.qtm = Qtm(self.plc, self.gui, 'qtm')

            self.waveSimulator = WaveSimulator(self.plc, self.gui)
            self.dataLogger = DataLogger(self.plc, self.gui)



        # Stop button A
        self.gui.stopButtonA.setIconSize(self.gui.stopButtonA.size())
        self.gui.stopButtonA.clicked.connect(self.slot_bStop)
        self.gui.stopButtonA.setStyleSheet(
            """
                QPushButton {
                    border-image: url(./icons/stop.png);
                    background-repeat: no-repeat;
                    background-color: white;
                    color: white;
                    border: none;
                    outline: none;
                }
                QPushButton:hover {
                    border-image: url(./icons/stop-hover.png);
                    background-repeat: no-repeat;
                    background-color: white;
                    outline: none;
                }
            """
        )

        # Stop button B
        self.gui.stopButtonB.setIconSize(self.gui.stopButtonB.size())
        self.gui.stopButtonB.clicked.connect(self.slot_bStop)
        self.gui.stopButtonB.setStyleSheet(
            """
                QPushButton {
                    border-image: url(./icons/stop.png);
                    background-repeat: no-repeat;
                    background-color: white;
                    color: white;
                    border: none;
                    outline: none;
                }
                QPushButton:hover {
                    border-image: url(./icons/stop-hover.png);
                    background-repeat: no-repeat;
                    background-color: white;
                    outline: none;
                }
            """
        )

        # PLC -> SIGNAL
        self.plcNotification('MAIN.eState', pyads.PLCTYPE_USINT, self.signal_eState)
        
        # SIGNAL -> SLOT
        self.signal_eState.connect(self.slot_eState)

        # Error popup
        self.msg = QtWidgets.QMessageBox()
        self.msg.setWindowTitle("MotionLab ERROR")
        self.msg.setText("Click OK to Acknowledge ERROR!")
        self.msg.setIcon(QtWidgets.QMessageBox.Critical)
        self.msg.buttonClicked.connect(self.startErrorCheck)
        
        # OpenGL
        text = open('./src/calib.json').read()
        calib = json.loads(text)
        # self.visualizer = MotionLabVisualizer(calib)
        
        # Initial log message
        self.logMessage('HMI Started')

        # Timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.errorCheck)
        
        self.show()

    @QtCore.pyqtSlot(int)
    def slot_eState(self, var):
        eState = E_MotionLabState(var)

        self.logMessage('Motion Lab is in ' + eState.name + ' mode')
        
        if eState != E_MotionLabState.NORMAL:
            # Show error message
            self.msg.exec_()


    def startErrorCheck(self):
        # Send reset to PLC and start timer for check
        self.timer.start(5000)        
        self.plc.write_by_name('MAIN.bReset', True, pyads.PLCTYPE_BOOL)

    def errorCheck(self):
        # Check if eState is NORMAL
        eState = E_MotionLabState(self.plc.read_by_name('MAIN.eState', pyads.PLCTYPE_USINT))

        # Stop timer
        self.timer.stop()

        if eState != E_MotionLabState.NORMAL:
            # Show popup again if not returned to NORMAL
            self.msg.exec_()

    
    def logMessage(self, message):
        now = datetime.now()
        date_time = str(now.strftime("[%d.%m.%Y-%H:%M:%S]: "))
        self.gui.logDump.insertPlainText(date_time +  message + '\n')
        self.gui.logDump.ensureCursorVisible()

    @QtCore.pyqtSlot()
    def slot_bStop(self):
        self.plc.write_by_name('MAIN.bStop', True, pyads.PLCTYPE_BOOL)
        self.logMessage('Stop pressed from HMI!')


    def plcNotification(self, adsName, plcType, pyqtSignal):
        # General callback function
        @notification(plcType, pyqtSignal)
        def callback(handle, name, timestamp, value):
            pass    

        attrib = pyads.NotificationAttrib(
            length=sizeof(plcType)
            # trans_mode=pyads.ADSTRANS_SERVERONCHA,
            # max_delay=10, # Max delay in ms
            # cycle_time=5 # Cycle time in ms
        )

        # Add notification to ads
        self.plc.add_device_notification(
            adsName,
            attrib,
            callback
        )

    # Function to handle the closing event of to the application
    def closeEvent(self, event):
        # reply = QMessageBox.question(self, 'Message',
        #     "Are you sure to quit?", QMessageBox.Yes |
        # QMessageBox.No, QMessageBox.No)
        reply = QtWidgets.QMessageBox.Yes
        

        self.em1500.close()
        self.em8000.close()
        self.comau.close()
        self.winch.close()
        self.dataLogger.close()


        if reply == QtWidgets.QMessageBox.Yes:
            
            if self.plcActive:
                # Close ADS ports
                self.plc.close()

            # Stop xbox thread
            self.xbox.close()

            event.accept()
        else:
            event.ignore()
            
           
        