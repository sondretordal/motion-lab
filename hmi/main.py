import sys


from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QMessageBox
from PyQt5 import uic
import pyads

gui_main_file = './gui/main.ui' # Enter file here.
gui_main, QtBaseClass = uic.loadUiType(gui_main_file)

class MyApp(QMainWindow):
    def __init__(self):
        # Open ADS Port
        pyads.open_port();

        # Set PLC ADS address
        self.adr = pyads.AmsAddr('192.168.90.150.1.1', 851)

        super(MyApp,self).__init__()
        self.ui = gui_main()
        self.ui.setupUi(self)

        self.ui.EM1500_settled.clicked.connect(self.EM1500_settled)
        self.ui.EM1500_neutral.clicked.connect(self.EM1500_neutral)
        self.ui.EM1500_engaged.clicked.connect(self.EM1500_engaged)

        self.ui.EM8000_settled.clicked.connect(self.EM8000_settled)
        self.ui.EM8000_neutral.clicked.connect(self.EM8000_neutral)
        self.ui.EM8000_engaged.clicked.connect(self.EM8000_engaged)

        self.ui.COMAU_settled.clicked.connect(self.COMAU_settled)
        self.ui.COMAU_engaged.clicked.connect(self.COMAU_engaged)
        self.ui.COMAU_engaged_fast.clicked.connect(self.COMAU_engaged_fast)

        self.ui.COMAU_omega.valueChanged.connect(self.COMAU_omega)

    def EM1500_settled(self):
        pyads.write_by_name(self.adr, 'EM1500.Control.CMND', 1, pyads.PLCTYPE_DINT)

    def EM1500_neutral(self):
        pyads.write_by_name(self.adr, 'EM1500.Control.CMND', 3, pyads.PLCTYPE_DINT)

    def EM1500_engaged(self):
        pyads.write_by_name(self.adr, 'EM1500.Control.CMND', 7, pyads.PLCTYPE_DINT)


    def EM8000_settled(self):
        pyads.write_by_name(self.adr, 'EM8000.Control.CMND', 1, pyads.PLCTYPE_DINT)

    def EM8000_neutral(self):
        pyads.write_by_name(self.adr, 'EM8000.Control.CMND', 3, pyads.PLCTYPE_DINT)

    def EM8000_engaged(self):
        pyads.write_by_name(self.adr, 'EM8000.Control.CMND', 7, pyads.PLCTYPE_DINT)

    def COMAU_settled(self):
        pyads.write_by_name(self.adr, 'COMAU.Control.mode', 0, pyads.PLCTYPE_DINT)

    def COMAU_engaged(self):
        pyads.write_by_name(self.adr, 'COMAU.Control.mode', 1, pyads.PLCTYPE_DINT)

    def COMAU_engaged_fast(self):
        pyads.write_by_name(self.adr, 'COMAU.Control.mode', 2, pyads.PLCTYPE_DINT)

    def COMAU_omega(self):
        omega = self.ui.COMAU_omega.value()
        self.ui.progressBar.setValue(omega)
        pyads.write_by_name(self.adr, 'COMAU.Control.omega', omega, pyads.PLCTYPE_REAL)

    def CloseADS(self):
        # Close ADS port
        pyads.close_port()
        print('Beckhoff ADS Connection Closed')

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes |
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.CloseADS()


            event.accept()
        else:
            event.ignore()


def main():

    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    app.exec_()



if __name__ == '__main__':
    main()
