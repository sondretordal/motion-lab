# Add subfolders to PYTHONPATH
import sys
from PyQt5 import QtWidgets
from RemoteInterface import RemoteInterface

# Main function
def main():
    app = QtWidgets.QApplication(sys.argv)
    remoteInterface = RemoteInterface()

    sys.exit(app.exec_())
    

# Application startup
if __name__ == '__main__':
    main()