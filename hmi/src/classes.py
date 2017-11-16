import numpy as np
from scipy.optimize import curve_fit

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



class RealTimeBar(object):
    def __init__(self):
        self.bars = []
        self.max_values = []

    def update(self, values):
        if len(values) == len(self.bars):
            for i in range(0, len(self.bars)):
                self.bars[i].setValue(values[i]/self.max_values[i]*100.0)
        else:
            print('Dimension mismatch')


class WaveSpectrum(object):
    def __init__(self, Hs=8.0, T1=12.0, spec='JONSWAP'):
        # Input parameters
        self.Hs = Hs
        self.T1 = T1
        self.spec = spec

        # Calculated parameters
        self.w = []
        self.S = []
        self.Slin = []
        self.w0 = []
        self.sigma = []
        self.Lambda = []

        # Initial parameter calculation
        self.calculate(self.Hs, self.T1, self.spec)

    def calculate(self, Hs, T1, spec):
        # Inital frequency range
        N = 100
        w_min = 0.01
        w_max = np.pi/2
        
        self.w = np.linspace(w_min, w_max, N)
        self.S = np.zeros(N)            
        # Calculate wavespectrum
        if spec == 'PMS':
            for k in range(0, N):
                # From average wave period to zero crossing period
                Tz = 0.921*T1
                
                # PM constants
                A = 4*np.pi**3*Hs**2/(Tz**4)
                B = 16*np.pi**3/(Tz**4)
                
                # Calculate wave spectrum 
                self.S[k] = A/(self.w[k]**5)*np.exp(-B/(self.w[k]**4))
                
        elif spec == 'JONSWAP':
            for k in range(0, N):
                if self.w[k] <= 5.24/T1:
                    sigma = 0.07
                else:
                    sigma = 0.09
                    
                Y = np.exp(-((0.191*self.w[k]*T1-1)/(np.sqrt(2)*sigma))**2)
                
                # Calculate wave spectrum
                self.S[k] = 155*Hs**2/(T1**4*self.w[k]**5)*np.exp(-944/(T1**4*self.w[k]**4))*3.3**Y
        
        # Update frequency range
        self.w0 = self.w[np.argmax(self.S)]

            
        # Approximate linear wave spectrum
        def linear_spectrum(w, p, w0, sigma):
            S = np.zeros(len(w))
            for k in range(0, len(w)):
                S[k] = 4*(p*w0*sigma*w[k])**2/((w0**2-w[k]**2)**2+4*(p*w0*w[k])**2)
                
            return S
        
        self.sigma = np.sqrt(max(self.S))
        
        # Find linearized curve parameters
        func = lambda w, par: linear_spectrum(self.w, par, self.w0, self.sigma)
        popt, pcov = curve_fit(func, self.w, self.S)
        
        # Ensure popt is positive
        self.Lambda = abs(popt[0])
        
        # Calculate linear approximated spectrum
        self.Slin = linear_spectrum(self.w, self.Lambda, self.w0, self.sigma)
        