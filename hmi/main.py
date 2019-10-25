# Add subfolders to PYTHONPATH
import sys
from PyQt5 import QtWidgets
from src.MotionLab import MotionLab

# Main function
def main():
    app = QtWidgets.QApplication(sys.argv)
    motionLab = MotionLab()

    sys.exit(app.exec_())
    

#Application startup
if __name__ == '__main__':
    main()