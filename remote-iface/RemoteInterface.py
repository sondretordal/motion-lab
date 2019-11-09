from PyQt5 import QtWidgets
from PyQt5 import QtCore
import pyqtgraph as pg
import numpy as np


from MainWindow import Ui_MainWindow
from RealTimePlot import RealTimePlot


class RemoteInterface(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(RemoteInterface, self).__init__()
        self.gui = Ui_MainWindow()
        self.gui.setupUi(self)


        self.timer = QtCore.QBasicTimer()
        

        self.show()


