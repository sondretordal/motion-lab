import numpy as np
import pyqtgraph as pg

class RealTimePlot(object):
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
            print('Dimension mismatch')

    def add_text_displays(self, displays):
        if len(self.curves) != 0:
            if len(displays) == len(self.curves):
                for i in range(0, len(displays)):
                    self.text_displays.append(displays[i])
            else:
                print('Dimension mismatch')
        else:
            print('Add curves before adding text displays')

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
            print('Dimension mismatch')

    def static_plot(self, t, y):
        for i in range(0, len(self.data)):
            self.curves[i].setData(t, y[i])
