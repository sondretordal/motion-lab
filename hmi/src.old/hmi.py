from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import pyqtgraph as pg
import time
import pyads
import numpy as np
import ctypes
import json
from scipy.optimize import curve_fit

from src.classes import RealTimePlot, RealTimeBar, WaveSpectrum
from src.datastructures import TxHmi, RxHmi, E_StewartMode
from src.gui import Ui_main
from src.opengl import MotionLabVisualizer

# Motionlab pybind module
from lib import motionlab as ml

# Background color pyqtgraph
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
pg.setConfigOptions(antialias=True)

class GUI(QMainWindow, Ui_main):
    def __init__(self):
        super(GUI, self).__init__()
        Ui_main.__init__(self)
        # Calling the initUI function
        self.initUI()

    # Function that initialize all the objects in the UI
    def initUI(self):
        # Set up the user interface from QT Designer
        self.setupUi(self)

        # Start ADS communications
        self.plc = pyads.Connection('192.168.90.150.1.1', 851)
        self.plc.open()

        try:
            self.plc.read_state()
            self.plc_active = True
        except pyads.ADSError:
            self.plc_active = False

        # Xbox controller
        self.xbox = ml.XboxController()
        self.xbox.start()

        self.EM1500_neutral_btn.clicked.connect(self.EM1500_settled)


    def EM1500_settled(self):
        self.plc.write_by_name('MAIN.em1500.eMode', 1, pyads.PLCTYPE_UINT)
        



    # Function to handle the closing event of to the application
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes |
        QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            

            if self.plc_active:
                # # Close ADS ports
                self.plc.close()
                print('Beckhoff ADS Connection Closed')

            # Stop xbox thread
            self.xbox.close()

            event.accept()
        else:
            event.ignore()
            
           
        