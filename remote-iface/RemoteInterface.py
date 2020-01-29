from PyQt5 import QtWidgets
from PyQt5 import QtCore
import pyqtgraph as pg
import numpy as np
import socket
from ctypes import *
import time

from MainWindow import Ui_MainWindow
from RealTimePlot import RealTimePlot

# PLC UDP Data Types import
from ST_TxUdpRemote import ST_TxUdpRemote
from ST_RxUdpRemote import ST_RxUdpRemote

class RemoteInterface(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(RemoteInterface, self).__init__()
        self.gui = Ui_MainWindow()
        self.gui.setupUi(self)

        # Udp Socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('192.168.90.60', 50060))

        # UPD data comm with PLC
        self.txData = ST_RxUdpRemote() # Send "ST_RxUdpRemote" type to PLC
        self.rxData = ST_TxUdpRemote() # Recv "ST_TxUdpRemote" type from PLC

        # Connect sliders
        self.gui.comau_u_0.sliderReleased.connect(lambda: self.gui.comau_u_0.setValue(0))
        self.gui.comau_u_1.sliderReleased.connect(lambda: self.gui.comau_u_1.setValue(0))
        self.gui.comau_u_2.sliderReleased.connect(lambda: self.gui.comau_u_2.setValue(0))
        self.gui.comau_u_3.sliderReleased.connect(lambda: self.gui.comau_u_3.setValue(0))
        self.gui.comau_u_4.sliderReleased.connect(lambda: self.gui.comau_u_4.setValue(0))
        self.gui.comau_u_5.sliderReleased.connect(lambda: self.gui.comau_u_5.setValue(0))


        self.gui.winch_u.sliderReleased.connect(lambda: self.gui.winch_u.setValue(0))

        # Udp Read/Write thread
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(50)

        # Initial time
        self.t0 = time.time()

        # Start GUI
        self.show()

    def update(self):
        # Elapsed time
        t = self.t0 - time.time()

        # Read data from udp
        data, addr = self.sock.recvfrom(1024) 
        memmove(addressof(self.rxData), data, sizeof(self.rxData))


        # Incerement counter
        self.txData.iCounter = self.txData.iCounter + 1

        self.txData.em1500_u[2] = 0.1*np.sin(0.1*2.0*np.pi*t)

        # self.txData.em1500_u[2] = self.gui.em1500_heavePos.value()

        # Comau speed setpoints
        for i in range(0, len(self.txData.comau_u)):
            qDotRef = eval('self.gui.comau_u_' + str(i)).value()/10.0/180.0*np.pi
            self.txData.comau_u[i] = qDotRef

        
        

        # Send data to PLC
        self.sock.sendto(self.txData, ('192.168.90.50', 50050))



    def closeEvent(self, event):
        self.timer.stop()
