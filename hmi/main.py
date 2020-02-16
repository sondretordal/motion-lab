# Add subfolders to PYTHONPATH
import sys
import qdarkstyle
from PyQt5 import QtWidgets
from src.MotionLab import MotionLab

from src.Remote import Remote

# Main function
def main():
    app = QtWidgets.QApplication(sys.argv)
    # app.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))

    motionLab = MotionLab()

    if motionLab.plcActive:
        remote = Remote(motionLab.plc, motionLab.gui, 'remote', motionLab)

    sys.exit(app.exec_())
    

# Application startup
if __name__ == '__main__':
    main()