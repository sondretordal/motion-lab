from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import pyqtgraph as pg
import time
import pyads
import numpy as np
import ctypes
from ctypes import sizeof
import json
from scipy.optimize import curve_fit

from src.classes import RealTimePlot, RealTimeBar, WaveSpectrum
from src.datastructures import TxHmi, RxHmi

from src.opengl import MotionLabVisualizer

# NEW
from .MainWindow import Ui_MainWindow
from .AdsQt import notification
from .StewartPlattform import *

# Motionlab pybind module
from lib import motionlab as ml

# Background color pyqtgraph
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
pg.setConfigOptions(antialias=True)

class MotionLab(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MotionLab, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Start ADS communications
        self.plc = pyads.Connection('192.168.90.150.1.1', 851)
        self.plc.open()

        try:
            self.plc.read_state()
            self.plcActive = True

        except pyads.ADSError:
            self.plcActive = False
        
        # Connec equipement to UI
        if self.plcActive:
            self.em1500 = StewartPlattform(self.plc, self.ui, 'em1500')

        

        

        # Xbox controller
        self.xbox = ml.XboxController()
        self.xbox.start()

        # OpenGL
        text = open('./src/calib.json').read()
        calib = json.loads(text)
        # self.visualizer = MotionLabVisualizer(calib)

        self.addNotification(
            'MAIN.val',
            pyads.PLCTYPE_SINT,
            self.em1500.eState
        )
        
        # Setup plotEM1500
        self.plotEM1500_A = RealTimePlot(self.ui._plotEM1500.addPlot())
        self.plotEM1500_A.plot.setLabel('left', 'Position', 'm')
        self.plotEM1500_A.plot.setYRange(-0.5, 0.5)
        self.plotEM1500_A.add_curves(['r', 'g', 'b'], ['Surge', 'Sway', 'Heave'])
        self.ui._plotEM1500.nextRow()
        self.plotEM1500_B = RealTimePlot(self.ui._plotEM1500.addPlot())
        self.plotEM1500_B.plot.setLabel('left', 'Angle', 'deg')
        self.plotEM1500_B.plot.setYRange(-6.0, 6.0)
        self.plotEM1500_B.add_curves(['r', 'g', 'b'], ['Roll', 'Pitch', 'Yaw'])

        self.plotEM8000_A = RealTimePlot(self.ui._plotEM8000.addPlot())
        self.plotEM8000_A.plot.setLabel('left', 'Position', 'm')
        self.plotEM8000_A.plot.setYRange(-0.5, 0.5)
        self.plotEM8000_A.add_curves(['r', 'g', 'b'], ['Surge', 'Sway', 'Heave'])
        self.ui._plotEM8000.nextRow()
        self.plotEM8000_B = RealTimePlot(self.ui._plotEM8000.addPlot())
        self.plotEM8000_B.plot.setLabel('left', 'Angle', 'deg')
        self.plotEM8000_B.plot.setYRange(-6.0, 6.0)
        self.plotEM8000_B.add_curves(['r', 'g', 'b'], ['Roll', 'Pitch', 'Yaw'])


        self.show()

    
    def addNotification(self, adsName, plcType, pyqtSignal):

        # General callback function
        @notification(plcType, pyqtSignal)
        def callback(handle, name, timestamp, value):
            pass

        # Add notification to ads
        self.plc.add_device_notification(
            adsName,
            pyads.NotificationAttrib(sizeof(plcType)),
            callback
        )


    # Function to handle the closing event of to the application
    def closeEvent(self, event):
        # reply = QMessageBox.question(self, 'Message',
        #     "Are you sure to quit?", QMessageBox.Yes |
        # QMessageBox.No, QMessageBox.No)
        reply = QMessageBox.Yes

        if reply == QMessageBox.Yes:
            
            if self.plcActive:
                # Close ADS ports
                self.plc.close()

            # Stop xbox thread
            self.xbox.close()

            event.accept()
        else:
            event.ignore()
            
           
        