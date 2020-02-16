from PyQt5 import QtCore
import numpy as np
import os
import errno
from ctypes import Structure
import csv
import pyads
import time
from enum import Enum

from .RealTimePlot import RealTimePlot



class DataLogger(QtCore.QObject):
    i = 0

    def __init__(self, plc, gui, parent=None):
        super(QtCore.QObject, self).__init__(parent)
        self.plc = plc
        self.gui = gui

        # Timer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update)

        # Connect GUIs
        self.gui.btnStartLog.clicked.connect(self.startLog)
        self.gui.btnStopLog.clicked.connect(self.stopLog)


    def startLog(self):
        # Write message on log started
        self.plc.write_by_name('GVL.logMessage', 'CSV logging started', pyads.PLCTYPE_STRING)

        # Set log amsple count to zero
        self.i = 0

        # Read destination file name
        filename = self.gui.logFilePath.text()

        # Create directory if non-existing
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        
        # Open file
        self.file = open(filename, 'w', newline='')
        self.writer = csv.writer(self.file)

        # Write CSV log header
        self.writer.writerow([
            'time',
            'em8000.surge',
            'sway [m]',
            'heave [m]',
            'roll [m]',
            'pitch [m]',
            'yaw [m]',
            'a [m]',
            'b [m]',
            'c [m]'
        ])

        # Get PLC data handle
        self.hData = self.plc.get_handle('MAIN.data')

        # Set log timing
        self.t0 = time.time()
        self.t1 = self.t0 + self.gui.logEndTime.value()
        self.gui.logProgress.setValue(0)

        # Start timer
        self.timer.start(50)

    def stopLog(self):
        # Write message on log started
        self.plc.write_by_name('GVL.logMessage', 'CSV logging ended', pyads.PLCTYPE_STRING)

        # Stop timer
        self.timer.stop()

        # Close log file
        if hasattr(self, 'file'):
            self.file.close()
        
    
    def update(self):
        t = time.time()

        if t <= self.t1:
            # Read data from PLC using ADS
            data = self.plc.read_by_name('', pyads.PLCTYPE_ARR_REAL(10), handle=self.hData)
            
            # Round off decimals
            data[0] = t - self.t0
            data = np.around(np.array(data), 4)

            # Increment log sample count
            self.i = self.i + 1
            
            # Write data to CSV file
            self.writer.writerow(data)

            # Update log progress bar and log sample count
            self.gui.logSampleCount.setText(str(self.i))
            self.gui.logProgress.setValue(int((t - self.t0)/(self.t1 - self.t0)*100))

        else:
            # Auto stop log when finished
            self.stopLog()

            # Set log progress bar to finished
            self.gui.logProgress.setValue(100)
     

    def setupPlot(self):
        self.plotInput = RealTimePlot(self.gui.comau_plot.addPlot())
        self.plotInput.plot.setLabel('left', 'Input', 'deg/s')
        self.plotInput.plot.setYRange(-10, 10)
        self.plotInput.add_curves(
            ['b', 'g', 'r', 'c', 'm', 'y'],
            ['u1', 'u2', 'u3', 'u4', 'u5', 'u6']
        )

        self.gui.comau_plot.nextRow()
        self.plotAngles = RealTimePlot(self.gui.comau_plot.addPlot())
        self.plotAngles.plot.setLabel('left', 'Angles', 'deg')
        self.plotAngles.plot.setYRange(-120, 90)
        self.plotAngles.add_curves(
            ['b', 'g', 'r', 'c', 'm', 'y'],
            ['q1', 'q2', 'q3', 'q4', 'q5', 'q6']
        )

    def close(self):
        self.stopLog()
