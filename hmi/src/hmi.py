import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import numpy as np
import pyqtgraph as pg
import pyads
import csv

# Background color pyqtgraph
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

# Load Qt Designer UI file
gui_main_file = './src/main.ui'
gui_main, QtBaseClass = uic.loadUiType(gui_main_file)


class GUI(QMainWindow, gui_main):
    def __init__(self):
        super(GUI, self).__init__()

        # Calling the initUI function
        self.initUI()

    # Function that initialize all the objects in the UI
    def initUI(self):

        # Set up the user interface from QT Designer
        self.setupUi(self)

        # Variable declaration
        self.t = np.zeros(1000)
        self.y = np.zeros(1000)
        self.time_save = []
        self.data_save = []
        self.time_range = 15

        # Connect the interaction functionality of the GUI
        self.ui_connect()

        # Setup of the plotting tab
        self.plot_setup()

        # Start ADS communication
        self.open_ADS()
        self.t_start = pyads.read_by_name(self.adr, 'Main.t', pyads.PLCTYPE_REAL)

        # Timer function for plot update
        # (with specified timeout value of "50 ms")
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.timer.start(50)

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
        #self.save_plot_btn.clicked.connect(self.save_plot_data)

        # Logging Tab:
        #----------------------------------------------------------#
        # Testing checkBox and groupBox functions
        self.checkBox_general.stateChanged.connect(self.checkbox_func)
        self.checkBox_EM8000.stateChanged.connect(self.checkbox_func)
        self.checkBox_EM1500.stateChanged.connect(self.checkbox_func)
        self.checkBox_COMAU.stateChanged.connect(self.checkbox_func)

    # Setup of the plotting tab
    def plot_setup(self):

        # Prettier plots 
        # (may affect performance)
        #pg.setConfigOptions(antialias=True)
        #pg.setConfigOption('background', 'w')

        # EM8000 - Plot Setup
        #-----------------------------------------------------------------------#

        # Adding position-plot and angle-plot objects to plot widget
        self.EM8000_plot_pos = self.EM8000_plot.addPlot()
        self.EM8000_plot.nextRow()
        self.EM8000_plot_ang = self.EM8000_plot.addPlot()

        # Adding lables, legends and grid to plot objects
        self.EM8000_plot_pos.setLabel('left', 'Position', 'm')
        self.EM8000_plot_pos.setLabel('bottom', '')
        self.EM8000_plot_ang.setLabel('left', 'Angle', 'deg')
        self.EM8000_plot_ang.setLabel('bottom', 'Time (s)')

        self.EM8000_plot_pos.addLegend(size=None, offset=(30, 30))
        self.EM8000_plot_ang.addLegend(size=None, offset=(30, 30))

        self.EM8000_plot_pos.showGrid(x=True, y=True)
        self.EM8000_plot_ang.showGrid(x=True, y=True)

        # Setting vertical range of plot objects
        self.EM8000_plot_pos.setYRange(-1, 1)
        self.EM8000_plot_ang.setYRange(-1, 1)

        # Adding position curves to position plot
        self.EM8000_plot_pos_x = self.EM8000_plot_pos.plot(pen="r", name="Sway")
        self.EM8000_plot_pos_y = self.EM8000_plot_pos.plot(pen="g", name="Surge")
        self.EM8000_plot_pos_z = self.EM8000_plot_pos.plot(pen="b", name="Heave")

        # Adding angle curves to angle plot
        self.EM8000_plot_ang_r = self.EM8000_plot_ang.plot(pen="r", name="Roll")
        self.EM8000_plot_ang_p = self.EM8000_plot_ang.plot(pen="g", name="Pitch")
        self.EM8000_plot_ang_y = self.EM8000_plot_ang.plot(pen="b", name="Yaw")

        # EM1500 - Plot Setup
        #-----------------------------------------------------------------------#

        # Adding position-plot and angle-plot objects to plot widget
        self.EM1500_plot_pos = self.EM1500_plot.addPlot()
        self.EM1500_plot.nextRow()
        self.EM1500_plot_ang = self.EM1500_plot.addPlot()

        # Adding lables, legends and grid to plot objects
        self.EM1500_plot_pos.setLabel('left', 'Position', 'm')
        self.EM1500_plot_pos.setLabel('bottom', '')
        self.EM1500_plot_ang.setLabel('left', 'Angle', 'deg')
        self.EM1500_plot_ang.setLabel('bottom', 'Time (s)')

        self.EM1500_plot_pos.addLegend(size=None, offset=(30, 30))
        self.EM1500_plot_ang.addLegend(size=None, offset=(30, 30))

        self.EM1500_plot_pos.showGrid(x=True, y=True)
        self.EM1500_plot_ang.showGrid(x=True, y=True)

        # Setting vertical range of plot objects
        self.EM1500_plot_pos.setYRange(-1, 1)
        self.EM1500_plot_ang.setYRange(-1, 1)

        # Adding position curves to position plot
        self.EM1500_plot_pos_x = self.EM1500_plot_pos.plot(pen="r", name="Sway")
        self.EM1500_plot_pos_y = self.EM1500_plot_pos.plot(pen="g", name="Surge")
        self.EM1500_plot_pos_z = self.EM1500_plot_pos.plot(pen="b", name="Heave")

        # Adding angle curves to angle plot
        self.EM1500_plot_ang_r = self.EM1500_plot_ang.plot(pen="r", name="Roll")
        self.EM1500_plot_ang_p = self.EM1500_plot_ang.plot(pen="g", name="Pitch")
        self.EM1500_plot_ang_y = self.EM1500_plot_ang.plot(pen="b", name="Yaw")

        # Initialize the output fields
        self.EM1500_output_pos_x.setText('0')
        self.EM1500_output_pos_y.setText('0')
        self.EM1500_output_pos_z.setText('0')
        self.EM1500_output_ang_r.setText('0')
        self.EM1500_output_ang_p.setText('0')
        self.EM1500_output_ang_y.setText('0')

        # COMAU - Plot Setup
        #-----------------------------------------------------------------------#

        # Adding position-plot object to plot widget
        self.COMAU_plot_pos = self.COMAU_plot.addPlot()

        # Adding lables, legend and grid to plot object
        self.COMAU_plot_pos.setLabel('left', 'Position', 'm')
        self.COMAU_plot_pos.setLabel('bottom', 'Time (s)')

        self.COMAU_plot_pos.addLegend(size=None, offset=(30, 30))

        self.COMAU_plot_pos.showGrid(x=True, y=True)

        # Setting vertical range of plot object
        self.COMAU_plot_pos.setYRange(-1, 7)

        # Adding position curves to position plot
        self.COMAU_plot_pos_j1 = self.COMAU_plot_pos.plot(pen="r", name="Joint 1")
        self.COMAU_plot_pos_j2 = self.COMAU_plot_pos.plot(pen="g", name="Joint 2")
        self.COMAU_plot_pos_j3 = self.COMAU_plot_pos.plot(pen="b", name="Joint 3")
        self.COMAU_plot_pos_j4 = self.COMAU_plot_pos.plot(pen="y", name="Joint 4")
        self.COMAU_plot_pos_j5 = self.COMAU_plot_pos.plot(pen="m", name="Joint 5")
        self.COMAU_plot_pos_j6 = self.COMAU_plot_pos.plot(pen="c", name="Joint 6")

        # Initialize the output fields
        self.COMAU_output_pos_j1.setText('0')
        self.COMAU_output_pos_j2.setText('0')
        self.COMAU_output_pos_j3.setText('0')
        self.COMAU_output_pos_j4.setText('0')
        self.COMAU_output_pos_j5.setText('0')
        self.COMAU_output_pos_j6.setText('0')

    # Update data and plot
    def update_data(self):

        # ADS read from PLC:
        time_plc = pyads.read_by_name(self.adr, 'Main.t', pyads.PLCTYPE_REAL)
        data = pyads.read_by_name(self.adr, 'Main.test', pyads.PLCTYPE_REAL)

        # Making the plot start at 0
        time = time_plc - self.t_start

        # Shifting data arrays
        self.t[:-1] = self.t[1:]
        self.t[-1] = time

        self.y[:-1] = self.y[1:]
        self.y[-1] = data

        # Append obtained ADS data
        # self.time_save.append(time)
        # self.data_save.append(data)
        
        self.COMAU_bar_j2.setValue(data*100.0)

        # EM8000 Plot Update
        #------------------------------------------------------------------------------#

        # Set the horizontal plot range
        # (the time-axis is a scrolling value, interval is determined by user input)
        self.EM8000_plot_pos.setXRange(time-self.time_range, time)
        self.EM8000_plot_ang.setXRange(time-self.time_range, time)

        # Plot data to related position curves
        self.EM8000_plot_pos_x.setData(self.t, self.y)
        self.EM8000_plot_pos_y.setData(self.t, 0.5*self.y)
        self.EM8000_plot_pos_z.setData(self.t, 0.25*self.y)

        # Plot data to related angle curves
        self.EM8000_plot_ang_r.setData(self.t, self.y)
        self.EM8000_plot_ang_p.setData(self.t, 0.5*self.y)
        self.EM8000_plot_ang_y.setData(self.t, 0.25*self.y)

        # Udpate the values in the output fields
        self.EM8000_output_pos_x.setText(str(data))
        self.EM8000_output_pos_y.setText(str(0.5*data))
        self.EM8000_output_pos_z.setText(str(0.25*data))
        self.EM8000_output_ang_r.setText(str(data))
        self.EM8000_output_ang_p.setText(str(0.5*data))
        self.EM8000_output_ang_y.setText(str(0.25*data))

        # EM1500 Plot Update
        #------------------------------------------------------------------------------#

        # Set the horizontal plot range
        # (the time-axis is a scrolling value, interval is determined by user input)
        self.EM1500_plot_pos.setXRange(time-self.time_range, time)
        self.EM1500_plot_ang.setXRange(time-self.time_range, time)

        # Plot data to related position curves
        self.EM1500_plot_pos_x.setData(self.t, self.y)
        self.EM1500_plot_pos_y.setData(self.t, 0.5*self.y)
        self.EM1500_plot_pos_z.setData(self.t, 0.25*self.y)

        # Plot data to related angle curves
        self.EM1500_plot_ang_r.setData(self.t, self.y)
        self.EM1500_plot_ang_p.setData(self.t, 0.5*self.y)
        self.EM1500_plot_ang_y.setData(self.t, 0.25*self.y)

        # Udpate the values in the output fields
        self.EM1500_output_pos_x.setText(str(data))
        self.EM1500_output_pos_y.setText(str(0.5*data))
        self.EM1500_output_pos_z.setText(str(0.25*data))
        self.EM1500_output_ang_r.setText(str(data))
        self.EM1500_output_ang_p.setText(str(0.5*data))
        self.EM1500_output_ang_y.setText(str(0.25*data))

        # COMAU Plot Update
        #------------------------------------------------------------------------------#

        # Set the horizontal plot range
        # (the time-axis is a scrolling value, interval is determined by user input)
        self.COMAU_plot_pos.setXRange(time-self.time_range, time)

        # Plot data to related position curves
        self.COMAU_plot_pos_j1.setData(self.t, self.y + 1)
        self.COMAU_plot_pos_j2.setData(self.t, self.y + 2)
        self.COMAU_plot_pos_j3.setData(self.t, self.y + 3)
        self.COMAU_plot_pos_j4.setData(self.t, self.y + 4)
        self.COMAU_plot_pos_j5.setData(self.t, self.y + 5)
        self.COMAU_plot_pos_j6.setData(self.t, self.y + 6)

        # Udpate the values in the output fields
        self.COMAU_output_pos_j1.setText(str(data + 1))
        self.COMAU_output_pos_j2.setText(str(data + 2))
        self.COMAU_output_pos_j3.setText(str(data + 3))
        self.COMAU_output_pos_j4.setText(str(data + 4))
        self.COMAU_output_pos_j5.setText(str(data + 5))
        self.COMAU_output_pos_j6.setText(str(data + 6))

       

    # Function to change the time axis range of the plots
    def plot_time_axis_range(self):
    # (This function is universal for all combobox objects in the plot tabs)

        # Set the time_range equal to combobox-object text
        self.time_range = int(self.sender().currentText())
        self.COMAU_bar_j1.setValue(self.time_range)
        # Find and set the selected index to all combobox objects in the plot tabs
        val = self.sender().currentIndex()
        self.EM8000_plot_time_range.setCurrentIndex(val)
        self.EM1500_plot_time_range.setCurrentIndex(val)
        self.COMAU_plot_time_range.setCurrentIndex(val)

    # Save plot data function
    def save_plot_data(self):

        data = zip(self.time_save, self.data_save)

        file_name = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;CSV Files (*.csv);;All Files (*)")
        if file_name[0]:
            with open(file_name[0], "w") as f:
                w = csv.writer(f, delimiter=",", lineterminator='\r\n')
                for row in data:
                    w.writerow(row)

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
        password, ok = QInputDialog.getText(self, "Login", "Please enter Password")
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

    # Open ADS connection to Beckhoff PLC
    def open_ADS(self):
        # Open ADS Port
        pyads.open_port()
        print "Beckhoff ADS Connection Open"

        # Set PLC ADS address
        self.adr = pyads.AmsAddr('192.168.90.150.1.1', 851)
        
    # Function to open file
    def file_open(self):
        self.tabWidget.setCurrentIndex(2)
        file_name = QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt);;Python Files (*.py);;All Files (*)")

        if file_name[0]:
            file = open(file_name[0], 'r')

            with file:
                text = file.read()
                self.text_edit.setText(text)

    # Function to save file
    def file_save(self):
        self.tabWidget.setCurrentIndex(2)
        file_name = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;Python Files (*.py);;All Files (*)")

        if file_name[0]:
            file = open(file_name[0], 'w')

            text = self.text_edit.toPlainText()
            file.write(text)
            file.close()

    # EM 8000 button functions
    def EM8000_settled(self):
        self.EM8000_settled_btn.setStyleSheet("background-color: #cccccc")
        self.EM8000_neutral_btn.setStyleSheet("background-color: none   ")
        self.EM8000_engaged_btn.setStyleSheet("background-color: none   ")

        #pyads.write_by_name(self.adr, 'EM8000.Control.CMND', 1, pyads.PLCTYPE_DINT)

    def EM8000_neutral(self):
        self.EM8000_settled_btn.setStyleSheet("background-color: none   ")
        self.EM8000_neutral_btn.setStyleSheet("background-color: #cccccc")
        self.EM8000_engaged_btn.setStyleSheet("background-color: none   ")

        #pyads.write_by_name(self.adr, 'EM8000.Control.CMND', 3, pyads.PLCTYPE_DINT)

    def EM8000_engaged(self):
        self.EM8000_settled_btn.setStyleSheet("background-color: none   ")
        self.EM8000_neutral_btn.setStyleSheet("background-color: none   ")
        self.EM8000_engaged_btn.setStyleSheet("background-color: #cccccc")

        #pyads.write_by_name(self.adr, 'EM8000.Control.CMND', 7, pyads.PLCTYPE_DINT)

    # EM 1500 button functions
    def EM1500_settled(self):
        self.EM1500_settled_btn.setStyleSheet("background-color: #cccccc")
        self.EM1500_neutral_btn.setStyleSheet("background-color: none")
        self.EM1500_engaged_btn.setStyleSheet("background-color: none")

        #pyads.write_by_name(self.adr, 'EM1500.Control.CMND', 1, pyads.PLCTYPE_DINT)

    def EM1500_neutral(self):
        self.EM1500_settled_btn.setStyleSheet("background-color: none   ")
        self.EM1500_neutral_btn.setStyleSheet("background-color: #cccccc")
        self.EM1500_engaged_btn.setStyleSheet("background-color: none   ")

        #pyads.write_by_name(self.adr, 'EM1500.Control.CMND', 3, pyads.PLCTYPE_DINT)

    def EM1500_engaged(self):
        self.EM1500_settled_btn.setStyleSheet("background-color: none   ")
        self.EM1500_neutral_btn.setStyleSheet("background-color: none   ")
        self.EM1500_engaged_btn.setStyleSheet("background-color: #cccccc")

        #pyads.write_by_name(self.adr, 'EM1500.Control.CMND', 7, pyads.PLCTYPE_DINT)

    # COMAU button functions
    def COMAU_settled(self):
        self.COMAU_settled_btn.setStyleSheet("background-color: #cccccc")
        self.COMAU_engaged_btn.setStyleSheet("background-color: none   ")
        self.COMAU_engaged_fast_btn.setStyleSheet("background-color: none")

        #pyads.write_by_name(self.adr, 'COMAU.Control.mode', 0, pyads.PLCTYPE_DINT)

    def COMAU_engaged(self):
        self.COMAU_settled_btn.setStyleSheet("background-color: none   ")
        self.COMAU_engaged_btn.setStyleSheet("background-color: #cccccc")
        self.COMAU_engaged_fast_btn.setStyleSheet("background-color: none")

        #pyads.write_by_name(self.adr, 'COMAU.Control.mode', 1, pyads.PLCTYPE_DINT)

    def COMAU_engaged_fast(self):
        self.COMAU_settled_btn.setStyleSheet("background-color: none")
        self.COMAU_engaged_btn.setStyleSheet("background-color: none")
        self.COMAU_engaged_fast_btn.setStyleSheet("background-color: #cccccc")

        #pyads.write_by_name(self.adr, 'COMAU.Control.mode', 2, pyads.PLCTYPE_DINT)

    # SYSTEM button functions
    def SYSTEM_settled(self):
        
        self.SYSTEM_settled_btn.setStyleSheet("background-color: #cccccc")
        self.EM8000_settled()
        self.EM1500_settled()
        self.COMAU_settled()

        print "system settled function is called"
        
    def SYSTEM_stop(self):
        self.SYSTEM_settled_btn.setStyleSheet("background-color: none")
        self.EM8000_settled()
        self.EM1500_settled()
        self.COMAU_settled()

        print "system stop function is called"
    # Close ADS connection to Bekchoff PLC
    def close_ADS(self):

        # Close ADS port
        pyads.close_port()
        print 'Beckhoff ADS Connection Closed'
    
    # Stop all function
    def stop_all(self):

        #pyads.write_by_name(self.adr, 'EM8000.Control.CMND', 1, pyads.PLCTYPE_DINT)
        #pyads.write_by_name(self.adr, 'EM1500.Control.CMND', 1, pyads.PLCTYPE_DINT)
        #pyads.write_by_name(self.adr, 'COMAU.Control.mode', 0, pyads.PLCTYPE_DINT)
        print 'APPLICATION STOPPED'

    # Function to handle the closing event of to the application
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes |
        QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.stop_all()
            self.close_ADS()
            event.accept()
        else:
            event.ignore()