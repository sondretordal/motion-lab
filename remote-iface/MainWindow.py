# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1304, 862)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menu_open_file = QtWidgets.QAction(MainWindow)
        self.menu_open_file.setObjectName("menu_open_file")
        self.menu_save_file = QtWidgets.QAction(MainWindow)
        self.menu_save_file.setObjectName("menu_save_file")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Remote Interface for Norwegian Motion Laboratory"))
        self.menu_open_file.setText(_translate("MainWindow", "Open File"))
        self.menu_open_file.setStatusTip(_translate("MainWindow", "Open File"))
        self.menu_open_file.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.menu_save_file.setText(_translate("MainWindow", "Save File"))
        self.menu_save_file.setStatusTip(_translate("MainWindow", "Save File"))
        self.menu_save_file.setShortcut(_translate("MainWindow", "Ctrl+S"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

