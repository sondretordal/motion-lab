import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QMessageBox
from PyQt5 import uic
import pyqtgraph
import pyads

qui_main_file = 'gui/main.ui' # Enter file here.
gui_main, QtBaseClass = uic.loadUiType(qui_main_file)
#hei jeg heter jan



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
        
    def EM1500_settled(self):
        pyads.write_by_name(self.adr, 'MotionLab.EM1500.Control.CMND', 1, pyads.PLCTYPE_DINT)
        
    def EM1500_neutral(self):
        pyads.write_by_name(self.adr, 'MotionLab.EM1500.Control.CMND', 3, pyads.PLCTYPE_DINT)
        
    def EM1500_engaged(self):
        pyads.write_by_name(self.adr, 'MotionLab.EM1500.Control.CMND', 7, pyads.PLCTYPE_DINT)
        
    def CloseADS(self):
        # Close ADS port
        pyads.close_port()
        print('ADS Connection Closed')

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            pyads.close_port()
            print('ADS Connection Closed')
            

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
    
    