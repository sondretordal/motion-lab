from PyQt5 import QtWidgets
from PyQt5 import QtCore
import pyqtgraph as pg
import numpy as np
import socket
from ctypes import *
import time

from MainWindow import Ui_MainWindow

# PLC UDP Data Types import
from RxUdp import RxUdp
from TxUdp import TxUdp

class RemoteInterface(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(RemoteInterface, self).__init__()
        self.gui = Ui_MainWindow()
        self.gui.setupUi(self)

        # Udp Socket
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(('192.168.90.60', 50060))

        # UPD data comm with PLC
        self.txData = TxUdp()
        self.rxData = RxUdp()

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

        # Apply sine motion to heave for EM1500
        self.txData.em1500_u[2] = 0.1*np.sin(0.1*2.0*np.pi*t)

        # Send data to PLC
        self.sock.sendto(self.txData, ('192.168.90.50', 50050))


    def closeEvent(self, event):
        self.timer.stop()
