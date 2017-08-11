import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import numpy as np
import pyqtgraph as pg
import pyads
import csv
import time
import socket
from ctypes import sizeof, memmove, byref, c_uint

from remotedata import TxData, RxData
import MotionLab

# Background color pyqtgraph
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

# Load Qt Designer UI file
gui_main_file = './src/main.ui'
gui_main, QtBaseClass = uic.loadUiType(gui_main_file)

##
class RealTimePlot:
    def __init__(self, plot):
        self.plot = plot
        self.curves = []
        self.text_displays = []
        self.buffer_size = 1000
        self.time = np.zeros(self.buffer_size)
        self.data = []
        self.time_range = 20
        self.precision = 4

        # Default setup for plot
        self.plot.showGrid(x=True, y=True)
        self.plot.addLegend(size=None, offset=(10, 10))
        self.plot.setLabel('bottom', 'Time - (s)')
        self.plot.setYRange(-1, 1)

    def add_curves(self, colors, names):
        if len(colors) == len(names):
            for i in range(0, len(colors)):
                curve = self.plot.plot(pen=colors[i], name=names[i])
                self.curves.append(curve)

                y = np.zeros(self.buffer_size)
                self.data.append(y)
        else:
            print "Dimension mismatch"

    def add_text_displays(self, displays):
        if len(self.curves) != 0:
            if len(displays) == len(self.curves):
                for i in range(0, len(displays)):
                    self.text_displays.append(displays[i])
            else:
                print "Dimension mismatch"
        else:
            print "Add curves before adding text displays"

    def update(self, t, y):
        self.time[0:-1] = self.time[1:]
        self.time[-1] = t

        self.plot.setXRange(self.time[-1] - self.time_range, self.time[-1])
        
        if len(y) == len(self.data):
            for i in range(0, len(self.data)):
                self.data[i][0:-1] = self.data[i][1:]
                self.data[i][-1] = y[i]
                
                self.curves[i].setData(self.time, self.data[i])

                if len(self.text_displays) == len(self.curves):
                    self.text_displays[i].setText(str(round(self.data[i][-1], self.precision)))

        else:
            print "Dimension mismatch"
##
class RealTimeBar:
    def __init__(self):
        self.bars = []
        self.max_values = []

    def update(self, values):
        if len(values) == len(self.bars):
            for i in range(0, len(self.bars)):
                self.bars[i].setValue(values[i]/self.max_values[i]*100.0)
        else:
            print "Dimension mismatch"

##
class UdpClient(RxData):
    def __init__(self, ip, port):
        self.addr = (ip, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(1)
        self.rx = RxData()
        self.hmi_counter = c_uint(0)
        self.server = []

        # Udp buffers
        self.__rx_buff = sizeof(RxData)
        self.__tx_buff = '0'*sizeof(self.hmi_counter)

    def update(self):
        # Send data to udp server
        memmove(self.__tx_buff, byref(self.hmi_counter), sizeof(self.hmi_counter))
        self.sock.sendto(self.__tx_buff, self.addr)
        
        # Recieve data from udp server
        try:
            self.__rx_buff, self.server = self.sock.recvfrom(sizeof(RxData))
            memmove(byref(self.rx), self.__rx_buff, sizeof(RxData))
        except timeout:
            print "Timeout"

        # Update hmi counter
        self.hmi_counter.value += 1

##
class GUI(QMainWindow, gui_main):
    def __init__(self):
        super(GUI, self).__init__()
        # Calling the initUI function
        self.initUI()

    # Function that initialize all the objects in the UI
    def initUI(self):
        # Set up the user interface from QT Designer
        self.setupUi(self)

        # Start ADS communication
        self.plc = pyads.Connection('192.168.90.150.1.1', 851)
        self.plc.open()
        print "Beckhoff ADS Connection Open"
        
        # Set PLC time to 0
        self.plc.write_by_name('REMOTE.Feedback.t', 0.0, pyads.PLCTYPE_REAL)

        # UDP server interface from pybind11
        #self.udp = UdpClient('192.168.90.50', 50150)
        self.udp = MotionLab.HmiInterface(50160)
        self.udp.start()

        # Real-time plots
        self.EM1500_1 = RealTimePlot(self.EM1500_plot.addPlot())
        self.EM1500_1.plot.setLabel('left', 'Position', 'm')
        self.EM1500_1.add_curves(['r', 'g', 'b'], ['Surge', 'Sway', 'Heave'])
        self.EM1500_1.add_text_displays([self.EM1500_output_pos_x, self.EM1500_output_pos_y, self.EM1500_output_pos_z])

        self.EM1500_plot.nextRow()

        self.EM1500_2 = RealTimePlot(self.EM1500_plot.addPlot())
        self.EM1500_2.plot.setLabel('left', 'Angle', 'deg')
        self.EM1500_2.add_curves(['r', 'g', 'b'], ['Roll', 'Pitch', 'Yaw'])
        self.EM1500_2.add_text_displays([self.EM1500_output_ang_r, self.EM1500_output_ang_p, self.EM1500_output_ang_y])
        
        self.EM8000_1 = RealTimePlot(self.EM8000_plot.addPlot())
        self.EM8000_1.plot.setLabel('left', 'Position', 'm')
        self.EM8000_1.add_curves(['r', 'g', 'b'], ['Surge', 'Sway', 'Heave'])
        self.EM8000_1.add_text_displays([self.EM8000_output_pos_x, self.EM8000_output_pos_y, self.EM8000_output_pos_z])

        self.EM8000_plot.nextRow()

        self.EM8000_2 = RealTimePlot(self.EM8000_plot.addPlot())
        self.EM8000_2.plot.setLabel('left', 'Angle', 'deg')
        self.EM8000_2.add_curves(['r', 'g', 'b'], ['Roll', 'Pitch', 'Yaw'])
        self.EM8000_2.add_text_displays([self.EM8000_output_ang_r, self.EM8000_output_ang_p, self.EM8000_output_ang_y])

        self.COMAU = RealTimePlot(self.COMAU_plot.addPlot())
        self.COMAU.plot.setYRange(-180, 180)
        self.COMAU.plot.setLabel('left', 'Angle', 'deg')
        self.COMAU.add_curves(['r', 'g', 'b', 'y', 'm', 'c'], ['q1', 'q2', 'q3', 'q4', 'q5', 'q6'])
        self.COMAU.add_text_displays([
                self.COMAU_output_pos_j1, self.COMAU_output_pos_j2, self.COMAU_output_pos_j3,
                self.COMAU_output_pos_j4, self.COMAU_output_pos_j5, self.COMAU_output_pos_j6
            ])

        # Joint stroke bar indicators
        self.EM1500_bars = RealTimeBar()
        self.EM1500_bars.max_values = [0.395]*12
        self.EM1500_bars.bars = [
                self.EM1500_bar1_l1, self.EM1500_bar1_l2, self.EM1500_bar1_l3, self.EM1500_bar1_l4, self.EM1500_bar1_l5, self.EM1500_bar1_l6,
                self.EM1500_bar2_l1, self.EM1500_bar2_l2, self.EM1500_bar2_l3, self.EM1500_bar2_l4, self.EM1500_bar2_l5, self.EM1500_bar2_l6
            ]
        
        self.EM8000_bars = RealTimeBar()
        self.EM8000_bars.max_values = [0.776]*12
        self.EM8000_bars.bars = [
                self.EM8000_bar1_l1, self.EM8000_bar1_l2, self.EM8000_bar1_l3, self.EM8000_bar1_l4, self.EM8000_bar1_l5, self.EM8000_bar1_l6,
                self.EM8000_bar2_l1, self.EM8000_bar2_l2, self.EM8000_bar2_l3, self.EM8000_bar2_l4, self.EM8000_bar2_l5, self.EM8000_bar2_l6
            ]
        
        self.COMAU_bars = RealTimeBar()
        self.COMAU_bars.max_values = [180]*12
        self.COMAU_bars.bars = [
                self.COMAU_bar1_j1, self.COMAU_bar1_j2, self.COMAU_bar1_j3, self.COMAU_bar1_j4, self.COMAU_bar1_j5, self.COMAU_bar1_j6,
                self.COMAU_bar2_j1, self.COMAU_bar2_j2, self.COMAU_bar2_j3, self.COMAU_bar2_j4, self.COMAU_bar2_j5, self.COMAU_bar2_j6
            ]

        # Plot time range setting
        self.time_range = 15

        # Connect the interaction functionality of the GUI
        self.ui_connect()

        # Timer function for plot update
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(35)

        # Set the relative path to the Sphinx docs
        dir1 = os.path.dirname(__file__)
        dir2 = os.path.dirname(dir1)
        dir3 = os.path.dirname(dir2)
        dir4 = os.path.abspath(dir3 + '\docs\_build\html\index.html')
        self.docView.load(QUrl.fromLocalFile(dir4))

        # Show UI
        self.show()

    # UI connections
    def ui_connect(self):
        # Password Protection of Tabs
        self.tabWidget.currentChanged.connect(self.tab_selector)

        # Interface Tab:
        #----------------------------------------------------------#
        # Connecting EM 8000 Interface-buttons to functions
        self.EM8000_settled_btn.clicked.connect(self.EM8000_settled)
        self.EM8000_neutral_btn.clicked.connect(self.EM8000_neutral)
        self.EM8000_engaged_btn.clicked.connect(self.EM8000_engaged)

        # Connecting EM 1500 Interface-buttons to functions
        self.EM1500_settled_btn.clicked.connect(self.EM1500_settled)
        self.EM1500_neutral_btn.clicked.connect(self.EM1500_neutral)
        self.EM1500_engaged_btn.clicked.connect(self.EM1500_engaged)

        # Connecting COMAU Interface-buttons to functions
        self.COMAU_settled_btn.clicked.connect(self.COMAU_settled)
        self.COMAU_engaged_btn.clicked.connect(self.COMAU_engaged)
        self.COMAU_engaged_fast_btn.clicked.connect(self.COMAU_engaged_fast)

        # Connecting SYSTEM Interface-buttons to functions
        self.SYSTEM_settled_btn.clicked.connect(self.SYSTEM_settled)
        self.SYSTEM_stop_btn.clicked.connect(self.SYSTEM_stop)

        # Plotting Tab:
        #----------------------------------------------------------#
        self.EM1500_plot_time_range.currentIndexChanged.connect(self.plot_time_axis_range)
        self.EM8000_plot_time_range.currentIndexChanged.connect(self.plot_time_axis_range)
        self.COMAU_plot_time_range.currentIndexChanged.connect(self.plot_time_axis_range)

        # Logging Tab:
        #----------------------------------------------------------#
        # Testing checkBox and groupBox functions
        self.checkBox_general.stateChanged.connect(self.checkbox_func)
        self.checkBox_EM8000.stateChanged.connect(self.checkbox_func)
        self.checkBox_EM1500.stateChanged.connect(self.checkbox_func)
        self.checkBox_COMAU.stateChanged.connect(self.checkbox_func)

    # Update data and plot
    def update_data(self):
        #self.udp.update()

        # Update real time plots
        self.EM1500_1.time_range = self.time_range
        self.EM1500_1.update(self.udp.Feedback.t, [
                self.udp.Feedback.EM1500.x, self.udp.Feedback.EM1500.y, self.udp.Feedback.EM1500.z
            ])
        self.EM1500_2.time_range = self.time_range
        self.EM1500_2.update(self.udp.Feedback.t, [
                self.udp.Feedback.EM1500.roll, self.udp.Feedback.EM1500.pitch, self.udp.Feedback.EM1500.yaw
            ])

        self.EM8000_1.time_range = self.time_range
        self.EM8000_1.update(self.udp.Feedback.t, [
                self.udp.Feedback.EM8000.x, self.udp.Feedback.EM8000.y, self.udp.Feedback.EM8000.z
            ])
        self.EM8000_2.time_range = self.time_range
        self.EM8000_2.update(self.udp.Feedback.t, [
                self.udp.Feedback.EM8000.roll, self.udp.Feedback.EM8000.pitch, self.udp.Feedback.EM8000.yaw
            ])
        
        self.COMAU.time_range = self.time_range
        self.COMAU.update(self.udp.Feedback.t, [
                self.udp.Feedback.COMAU.q1, self.udp.Feedback.COMAU.q2, self.udp.Feedback.COMAU.q3,
                self.udp.Feedback.COMAU.q4, self.udp.Feedback.COMAU.q5, self.udp.Feedback.COMAU.q6
            ])
        
        self.EM8000_bars.update([
                self.udp.Feedback.EM8000.L1, self.udp.Feedback.EM8000.L2, self.udp.Feedback.EM8000.L3,
                self.udp.Feedback.EM8000.L4, self.udp.Feedback.EM8000.L5, self.udp.Feedback.EM8000.L6,
                self.udp.Feedback.EM8000.L1, self.udp.Feedback.EM8000.L2, self.udp.Feedback.EM8000.L3,
                self.udp.Feedback.EM8000.L4, self.udp.Feedback.EM8000.L5, self.udp.Feedback.EM8000.L6
            ])

        self.EM1500_bars.update([
                self.udp.Feedback.EM1500.L1, self.udp.Feedback.EM1500.L2, self.udp.Feedback.EM1500.L3,
                self.udp.Feedback.EM1500.L4, self.udp.Feedback.EM1500.L5, self.udp.Feedback.EM1500.L6,
                self.udp.Feedback.EM1500.L1, self.udp.Feedback.EM1500.L2, self.udp.Feedback.EM1500.L3,
                self.udp.Feedback.EM1500.L4, self.udp.Feedback.EM1500.L5, self.udp.Feedback.EM1500.L6
            ])

        self.COMAU_bars.update([
                self.udp.Feedback.COMAU.q1, self.udp.Feedback.COMAU.q2, self.udp.Feedback.COMAU.q3,
                self.udp.Feedback.COMAU.q4, self.udp.Feedback.COMAU.q5, self.udp.Feedback.COMAU.q6,
                self.udp.Feedback.COMAU.q1, self.udp.Feedback.COMAU.q2, self.udp.Feedback.COMAU.q3,
                self.udp.Feedback.COMAU.q4, self.udp.Feedback.COMAU.q5, self.udp.Feedback.COMAU.q6
            ])

    # Function to change the time axis range of the plots
    def plot_time_axis_range(self):
    # (This function is universal for all combobox objects in the plot tabs)

        # Set the time_range equal to combobox-object text
        self.time_range = int(self.sender().currentText())

        # Find and set the selected index to all combobox objects in the plot tabs
        val = self.sender().currentIndex()
        self.EM8000_plot_time_range.setCurrentIndex(val)
        self.EM1500_plot_time_range.setCurrentIndex(val)
        self.COMAU_plot_time_range.setCurrentIndex(val)

    # Logging tab checkboxes
    def checkbox_func(self):
        selected_box = self.sender()

        if selected_box.text() == "General":
            if selected_box.isChecked() == True:
                
                self.groupBox_log_general.setEnabled(True)
            else:
                
                self.groupBox_log_general.setEnabled(False)
        if selected_box.text() == "EM8000":
            if selected_box.isChecked() == True:
                
                self.groupBox_log_EM8000.setEnabled(True)
            else:
                
                self.groupBox_log_EM8000.setEnabled(False)
        if selected_box.text() == "EM1500":
            if selected_box.isChecked() == True:
                
                self.groupBox_log_EM1500.setEnabled(True)
            else:
                
                self.groupBox_log_EM1500.setEnabled(False)

        if selected_box.text() == "COMAU":
            if selected_box.isChecked() == True:
                
                self.groupBox_log_COMAU.setEnabled(True)
            else:
                
                self.groupBox_log_COMAU.setEnabled(False)

    # Main Tab selector
    # (with password protection on admin-tab)
    def tab_selector(self):
        # Check if the selected tab is admin-tab
        # If so, call function "password_login(password)"
        main_tab = self.sender()
        if main_tab.currentIndex() == 4:
            if self.password_login("1234"):
                #print "Good Accepted"
                main_tab.setCurrentIndex(4)
            else:
                #print "Denied"
                main_tab.setCurrentIndex(0)

    # Password protection on tab
    def password_login(self, pw):
        password, ok = QInputDialog.getText(self, "Login", "Please enter Password", QLineEdit.Password)
        if ok:
            if password == pw:
                return True
            else:
                msg = QMessageBox(self)
                msg.setIcon(QMessageBox.Warning)
                msg.setText("Wrong Password, please try again")
                msg.setWindowTitle("Access Denied")
                msg.exec_()
                return False
        
    # EM 8000 button functions
    def EM8000_settled(self):
        self.EM8000_settled_btn.setStyleSheet("background-color: #cccccc")
        self.EM8000_neutral_btn.setStyleSheet("background-color: none   ")
        self.EM8000_engaged_btn.setStyleSheet("background-color: none   ")

        # Write to PLC: EM8000 settled = 1
        self.plc.write_by_name('EM8000.Control.CMND', 1, pyads.PLCTYPE_DINT)

    def EM8000_neutral(self):
        self.EM8000_settled_btn.setStyleSheet("background-color: none   ")
        self.EM8000_neutral_btn.setStyleSheet("background-color: #cccccc")
        self.EM8000_engaged_btn.setStyleSheet("background-color: none   ")

        # Write to PLC: EM8000 neutral = 3
        self.plc.write_by_name('EM8000.Control.CMND', 3, pyads.PLCTYPE_DINT)

    def EM8000_engaged(self):
        self.EM8000_settled_btn.setStyleSheet("background-color: none   ")
        self.EM8000_neutral_btn.setStyleSheet("background-color: none   ")
        self.EM8000_engaged_btn.setStyleSheet("background-color: #cccccc")

        # Write to PLC: EM8000 engaged = 7
        self.plc.write_by_name('EM8000.Control.CMND', 7, pyads.PLCTYPE_DINT)

    # EM 1500 button functions
    def EM1500_settled(self):
        self.EM1500_settled_btn.setStyleSheet("background-color: #cccccc")
        self.EM1500_neutral_btn.setStyleSheet("background-color: none")
        self.EM1500_engaged_btn.setStyleSheet("background-color: none")

        # Write to PLC: EM1500 settled = 1
        self.plc.write_by_name('EM1500.Control.CMND', 1, pyads.PLCTYPE_DINT)

    def EM1500_neutral(self):
        self.EM1500_settled_btn.setStyleSheet("background-color: none   ")
        self.EM1500_neutral_btn.setStyleSheet("background-color: #cccccc")
        self.EM1500_engaged_btn.setStyleSheet("background-color: none   ")

        # Write to PLC: EM1500 neutral = 3
        self.plc.write_by_name('EM1500.Control.CMND', 3, pyads.PLCTYPE_DINT)

    def EM1500_engaged(self):
        self.EM1500_settled_btn.setStyleSheet("background-color: none   ")
        self.EM1500_neutral_btn.setStyleSheet("background-color: none   ")
        self.EM1500_engaged_btn.setStyleSheet("background-color: #cccccc")

        # Write to PLC: EM1500 engaged = 7
        self.plc.write_by_name('EM1500.Control.CMND', 7, pyads.PLCTYPE_DINT)

    # COMAU button functions
    def COMAU_settled(self):
        self.COMAU_settled_btn.setStyleSheet("background-color: #cccccc")
        self.COMAU_engaged_btn.setStyleSheet("background-color: none   ")
        self.COMAU_engaged_fast_btn.setStyleSheet("background-color: none")

        # Write to PLC: COMAU settled = 1
        self.plc.write_by_name('COMAU.Control.mode', 0, pyads.PLCTYPE_DINT)

    def COMAU_engaged(self):
        self.COMAU_settled_btn.setStyleSheet("background-color: none   ")
        self.COMAU_engaged_btn.setStyleSheet("background-color: #cccccc")
        self.COMAU_engaged_fast_btn.setStyleSheet("background-color: none")

        # Write to PLC: COMAU engaged = 1
        self.plc.write_by_name('COMAU.Control.mode', 1, pyads.PLCTYPE_DINT)

    def COMAU_engaged_fast(self):
        self.COMAU_settled_btn.setStyleSheet("background-color: none")
        self.COMAU_engaged_btn.setStyleSheet("background-color: none")
        self.COMAU_engaged_fast_btn.setStyleSheet("background-color: #cccccc")

        # Write to PLC: COMAU engaged-fast = 2
        self.plc.write_by_name('COMAU.Control.mode', 2, pyads.PLCTYPE_DINT)

    # SYSTEM button functions
    def SYSTEM_settled(self):
        self.SYSTEM_settled_btn.setStyleSheet("background-color: #cccccc")
        self.EM8000_settled()
        self.EM1500_settled()
        self.COMAU_settled()

    def SYSTEM_stop(self):
        self.SYSTEM_settled_btn.setStyleSheet("background-color: none")
        self.EM8000_settled()
        self.EM1500_settled()
        self.COMAU_settled()

    # Stop all function
    def stop_all(self):

        self.SYSTEM_stop()
        print 'APPLICATION STOPPED'

    # Function to handle the closing event of to the application
    def closeEvent(self, event):
        # reply = QMessageBox.question(self, 'Message',
        #     "Are you sure to quit?", QMessageBox.Yes |
        # QMessageBox.No, QMessageBox.No)

        # if reply == QMessageBox.Yes:
        #     self.stop_all()
            
        #     # Close ADS port
        #     pyads.close_port()
        #     print 'Beckhoff ADS Connection Closed'

        #     self.sock.close()
        #     event.accept()
        # else:
        #     event.ignore()

            self.stop_all()
            
            # Close ADS port
            self.plc.close()
            print 'Beckhoff ADS Connection Closed'

            self.udp.close()
            print 'HMI Udp Connection Closed'

            event.accept()