import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5 import uic
import numpy as np
import pyqtgraph as pg
import pyads
import csv

gui_main_file = './src/gui/main.ui' # Enter file here. 
gui_main, QtBaseClass = uic.loadUiType(gui_main_file)

class GUI(QMainWindow,gui_main):
    def __init__(self):
        super(GUI,self).__init__()

        # Calling the initUI function
        self.initUI()

    # Function that initialize all the objects in the UI
    def initUI(self):

        # Set up the user interface from QT Designer
        self.setupUi(self)

        # Variable declaration
        a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        b = [10, 5, -5, 10, 2, 3, 4, 8, 9, 1]
        c = [13, 33, 4, 11, 2, 5, 20, 14, 14, 5]
        d = [1, 2, 5, 6, -2, 5, 6, -3, 1, 2]

        self.t = np.zeros(1000)
        self.y = np.zeros(1000)
        self.time_save = []
        self.data_save = []

        # Calling GUI connection function
        self.ui_connect()                               # Calling the function "ui_connect"
                                                        # This connects the functionality of the GUI

        # Start ADS communication
        self.open_ADS()                                 # Calling the function "open_ADS"

        # Timer function
        self.timer = QTimer()                           # Calling the timer QT widget
        self.timer.timeout.connect(self.update_plot)    # Connecting the timer timeout to "update_plot" function
        self.timer.start(50)                            # Start the timer with the timeout specified value: "50 ms"

        # Creating dummy plot

        #pg.setConfigOptions(antialias=True)             # Prettier plots (may affect performance)

        self.plotcurve = pg.PlotCurveItem()
        self.plotcurve2 = pg.PlotCurveItem()
        self.pyqtgraph_plot.addItem(self.plotcurve)
        self.pyqtgraph_plot.addItem(self.plotcurve2)

        #self.pyqtgraph_plot.plot(a, b)
        
        self.pyqtgraph_plot_2.plot(a, b)
        self.pyqtgraph_plot_3.plot(a, b)
        self.pyqtgraph_plot_4.plot(a, b)
        self.pyqtgraph_plot_5.plot(a, b)
        self.pyqtgraph_plot_11.plot(a, b)


        p1 = self.plot_EM1500.addPlot()
        p2 = self.plot_EM1500.addPlot()
        p3 = self.plot_EM1500.addPlot()
        self.plot_EM1500.nextRow()
        p4 = self.plot_EM1500.addPlot()
        p5 = self.plot_EM1500.addPlot()
        p6 = self.plot_EM1500.addPlot()
        curve1 = p1.plot(a, b)
        curve2 = p2.plot(a, c)
        curve3 = p3.plot(a, d)
        curve4 = p4.plot(a, b)
        curve5 = p5.plot(a, c)
        curve6 = p6.plot(a, d)

 
        self.p11 = self.plot_COMAU.addPlot()
        self.plot_COMAU.nextRow()
        self.p12 = self.plot_COMAU.addPlot()

        self.p12.addLegend(size=None, offset=(30, 30))
        self.p12.setLabel('bottom', 'Time', 's')
        self.p12.setLabel('left', 'Value')

        self.curve11 = self.p11.plot(pen="y")
        self.curve12 = self.p12.plot(pen="r", name="red")
        self.curve13 = self.p12.plot(pen="g", name="green")

        # Show UI
        self.show()

    # Update plot function
    def update_plot(self):

        # ADS read from PLC:
        time = pyads.read_by_name(self.adr, 'Main.t', pyads.PLCTYPE_REAL)
        data = pyads.read_by_name(self.adr, 'Main.test', pyads.PLCTYPE_REAL)

        # Shifting data arrays
        self.t[:-1] = self.t[1:]
        self.t[-1] = time

        self.y[:-1] = self.y[1:]
        self.y[-1] = data

        # Setup of Scrolling PlotWidget (EM8000)
        self.pyqtgraph_plot.setYRange(-1, 1)
        self.pyqtgraph_plot.setXRange(time-15, time)
        self.plotcurve.setData(self.t, self.y)
        self.plotcurve2.setData(self.t, 0.5*self.y)


        # Setup of Scrolling PlotWidget (COMAU)
        self.p11.setYRange(-1, 1)
        self.p11.setXRange(time-15, time)

        self.p12.setYRange(-1, 1)
        self.p12.setXRange(time-15, time)

        self.curve11.setData(self.t, self.y)
        self.curve12.setData(self.t, self.y)
        self.curve13.setData(self.t, 0.5*self.y)

        # Append obtained ADS data
        self.time_save.append(time)
        self.data_save.append(data)

    # Save plot data function
    def save_plot_data(self):

        # self.ui.textEdit_data.setText("")
        # self.ui.textEdit_time.setText("")

        # for i in range(0, len(self.time_save)):
        #     self.ui.textEdit_time.append(str(self.time_save[i]))
        #     self.ui.textEdit_data.append(str(self.data_save[i]))

        data = zip(self.time_save, self.data_save)

        file_name = QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt);;CSV Files (*.csv);;All Files (*)")
        if file_name[0]:
            with open(file_name[0], "w") as f:
                w = csv.writer(f, delimiter=",", lineterminator='\r\n')
                for row in data:
                    w.writerow(row)

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

        # Plotting Tab:
        #----------------------------------------------------------#
        self.save_plot_btn.clicked.connect(self.save_plot_data)

        # Logging Tab:
        #----------------------------------------------------------#
        # Testing checkBox and groupBox functions
        self.checkBox_general.stateChanged.connect(self.checkbox_func)
        self.checkBox_EM8000.stateChanged.connect(self.checkbox_func)
        self.checkBox_EM1500.stateChanged.connect(self.checkbox_func)
        self.checkBox_COMAU.stateChanged.connect(self.checkbox_func)

        # Menu bar:
        #----------------------------------------------------------#
        self.menu_open_file.triggered.connect(self.file_open)
        self.menu_save_file.triggered.connect(self.file_save)



    # Testing checkbox function
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

    # Testing tab selector function
    def tab_selector(self):
        main_tab = self.sender()
        if main_tab.currentIndex() == 4:
            if self.password_login("1234"):
                #print "Good Accepted"
                main_tab.setCurrentIndex(4)
            else:
                #print "Denied"
                main_tab.setCurrentIndex(0)

    # Testing Password protection on tab
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

    # Function to open ADS connection to Beckhoff PLC
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
        self.EM8000_settled_btn.setStyleSheet("QPushButton { background-color: #cccccc }")
        self.EM8000_neutral_btn.setStyleSheet("QPushButton { background-color: none    }")
        self.EM8000_engaged_btn.setStyleSheet("QPushButton { background-color: none    }")

        #pyads.write_by_name(self.adr, 'EM8000.Control.CMND', 1, pyads.PLCTYPE_DINT)

    def EM8000_neutral(self):
        self.EM8000_settled_btn.setStyleSheet("QPushButton { background-color: none    }")
        self.EM8000_neutral_btn.setStyleSheet("QPushButton { background-color: #cccccc }")
        self.EM8000_engaged_btn.setStyleSheet("QPushButton { background-color: none    }")

        #pyads.write_by_name(self.adr, 'EM8000.Control.CMND', 3, pyads.PLCTYPE_DINT)

    def EM8000_engaged(self):
        self.EM8000_settled_btn.setStyleSheet("QPushButton { background-color: none    }")
        self.EM8000_neutral_btn.setStyleSheet("QPushButton { background-color: none    }")
        self.EM8000_engaged_btn.setStyleSheet("QPushButton { background-color: #cccccc }")

        #pyads.write_by_name(self.adr, 'EM8000.Control.CMND', 7, pyads.PLCTYPE_DINT)

    # EM 1500 button functions
    def EM1500_settled(self):
        self.EM1500_settled_btn.setStyleSheet("background-color: #cccccc")
        self.EM1500_neutral_btn.setStyleSheet("background-color: none")
        self.EM1500_engaged_btn.setStyleSheet("background-color: none")

        #pyads.write_by_name(self.adr, 'EM1500.Control.CMND', 1, pyads.PLCTYPE_DINT)

    def EM1500_neutral(self):
        self.EM1500_settled_btn.setStyleSheet("QPushButton { background-color: none    }")
        self.EM1500_neutral_btn.setStyleSheet("QPushButton { background-color: #cccccc }")
        self.EM1500_engaged_btn.setStyleSheet("QPushButton { background-color: none    }")

        #pyads.write_by_name(self.adr, 'EM1500.Control.CMND', 3, pyads.PLCTYPE_DINT)

    def EM1500_engaged(self):
        self.EM1500_settled_btn.setStyleSheet("QPushButton { background-color: none    }")
        self.EM1500_neutral_btn.setStyleSheet("QPushButton { background-color: none    }")
        self.EM1500_engaged_btn.setStyleSheet("QPushButton { background-color: #cccccc }")

        #pyads.write_by_name(self.adr, 'EM1500.Control.CMND', 7, pyads.PLCTYPE_DINT)

    # COMAU button functions
    def COMAU_settled(self):
        self.COMAU_settled_btn.setStyleSheet("QPushButton { background-color: #cccccc }")
        self.COMAU_engaged_btn.setStyleSheet("QPushButton { background-color: none    }")
        self.COMAU_engaged_fast_btn.setStyleSheet("QPushButton { background-color: none    }")

        #pyads.write_by_name(self.adr, 'COMAU.Control.mode', 0, pyads.PLCTYPE_DINT)

    def COMAU_engaged(self):
        self.COMAU_settled_btn.setStyleSheet("QPushButton { background-color: none    }")
        self.COMAU_engaged_btn.setStyleSheet("QPushButton { background-color: #cccccc }")
        self.COMAU_engaged_fast_btn.setStyleSheet("QPushButton { background-color: none    }")

        #pyads.write_by_name(self.adr, 'COMAU.Control.mode', 1, pyads.PLCTYPE_DINT)

    def COMAU_engaged_fast(self):
        self.COMAU_settled_btn.setStyleSheet("QPushButton { background-color: none    }")
        self.COMAU_engaged_btn.setStyleSheet("QPushButton { background-color: none    }")
        self.COMAU_engaged_fast_btn.setStyleSheet("QPushButton { background-color: #cccccc }")

        #pyads.write_by_name(self.adr, 'COMAU.Control.mode', 2, pyads.PLCTYPE_DINT)

    # Function to close ADS connection to Bekchoff PLC
    def close_ADS(self):
        # Close ADS port
        pyads.close_port()
        print('Beckhoff ADS Connection Closed')

    # Function to handle the closing event of to the application
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes |
        QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.close_ADS()
            event.accept()
        else:
            event.ignore()

# # Main function
# def main():
#     app = QApplication(sys.argv)
#     window = GUI()
#     sys.exit(app.exec_())

# #Application startup
# if __name__ == '__main__':
#     main()