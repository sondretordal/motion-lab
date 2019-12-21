from PyQt5 import QtWidgets, QtCore, QtGui
import pyqtgraph as pg
import pyads
import json
from ctypes import sizeof
from datetime import datetime

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
from .Remote import Remote
from .Mru import Mru
from .Qtm import Qtm


# Motionlab pybind module
from lib import motionlab as ml

# Background color pyqtgraph
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
pg.setConfigOptions(antialias=True)


class MotionLab(QtWidgets.QMainWindow, Ui_MainWindow):
    signal_logMessage = QtCore.pyqtSignal(str)
    

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
            self.remote = Remote(self.plc, self.gui, 'remote')
            self.qtm = Qtm(self.plc, self.gui, 'qtm')

            self.waveSimulator = WaveSimulator(self.plc, self.gui)
            self.dataLogger = DataLogger(self.plc, self.gui)

            # Log Dump notification
            self.plc.write_by_name('GVL.logMessage', 'HMI Started', pyads.PLCTYPE_STRING)    
            self.plcNotification('GVL.logMessage', pyads.PLCTYPE_STRING, self.signal_logMessage)
            self.signal_logMessage.connect(self.slot_logMessage)
            


        # Stop button A
        self.gui.stopButtonA.setIconSize(self.gui.stopButtonA.size())
        self.gui.stopButtonA.clicked.connect(self.stopAll)
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
        self.gui.stopButtonB.clicked.connect(self.stopAll)
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

        # Xbox controller
        self.xbox = ml.XboxController()
        self.xbox.start()

        # OpenGL
        text = open('./src/calib.json').read()
        calib = json.loads(text)
        # self.visualizer = MotionLabVisualizer(calib)
        

        self.show()

    def stopAll(self):
        if self.plcActive:
            # TODO: Implement stop all in PLC
            self.plc.write_by_name('GVL.logMessage', 'Stop activated from HMI', pyads.PLCTYPE_STRING)
  
    @QtCore.pyqtSlot(str)
    def slot_logMessage(self, var):
        message = self.plc.read_by_name('GVL.logMessage', pyads.PLCTYPE_STRING)
        now = datetime.now()
        date_time = str(now.strftime("[%d.%m.%Y-%H:%M:%S]: "))
        self.gui.logDump.insertPlainText(date_time +  str(message) + '\n')
        self.gui.logDump.ensureCursorVisible()


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
            
           
        