from PyQt5 import QtWidgets, QtCore
import pyqtgraph as pg
import pyads
import json

# TODO: Implement this
from src.opengl import MotionLabVisualizer

# NEW
from .MainWindow import Ui_MainWindow
from .StewartPlattform import StewartPlattform
from .ComauRobot import ComauRobot
from .RobotWinch import RobotWinch
from .WaveSimulator import WaveSimulator
from .DataLogger import DataLogger


# Motionlab pybind module
from lib import motionlab as ml

# Background color pyqtgraph
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
pg.setConfigOptions(antialias=True)


class MotionLab(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MotionLab, self).__init__()
        self.gui = Ui_MainWindow()
        self.gui.setupUi(self)
        
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

            self.waveSimulator = WaveSimulator(self.plc, self.gui)
            self.dataLogger = DataLogger(self.plc, self.gui)


        # Xbox controller
        self.xbox = ml.XboxController()
        self.xbox.start()

        # OpenGL
        text = open('./src/calib.json').read()
        calib = json.loads(text)
        # self.visualizer = MotionLabVisualizer(calib)
        

        self.show()

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
            
           
        