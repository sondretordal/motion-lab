from enum import Enum
import numpy as np
import pyads
from scipy.optimize import curve_fit
from .RealTimePlot import RealTimePlot



class WaveSimulator(object):
    
    def __init__(self, plc, gui):
        self.plc = plc
        self.gui = gui
        
        # Wave spectrum plot
        self.spectrumPlot = RealTimePlot(self.gui.waveSpectrum_plot.addPlot())
        self.spectrumPlot.plot.setLabel('left', 'Wave Spectrum Density [m^2s]')
        self.spectrumPlot.plot.setLabel('bottom', 'Wave Frequency [Hz]')
        self.spectrumPlot.add_curves(['r', 'b'], ['Wave Spectrum', 'Linear Approximation'])
    
        # Initial wave spectrum
        self.spectrumChanged()
        

        # Conncet GUI elements
        self.gui.Hs.valueChanged.connect(self.spectrumChanged)
        self.gui.Tp.valueChanged.connect(self.spectrumChanged)
        self.gui.spectrumType.currentIndexChanged.connect(self.spectrumChanged)
        self.gui.bResetDofScaling.clicked.connect(self.resetScaling)

    def resetScaling(self):
        self.plc.write_by_name('MAIN.em1500.bResetScale', True, pyads.PLCTYPE_BOOL)
        self.plc.write_by_name('MAIN.em8000.bResetScale', True, pyads.PLCTYPE_BOOL)

    def spectrumChanged(self):
        # Get values from UI
        Hs = self.gui.Hs.value()
        Tp = self.gui.Tp.value()
        spec = E_SpectrumType(self.gui.spectrumType.currentIndex())

        # Calculate spectrum
        self.spectrum = WaveSpectrum(Hs, Tp, spec)

        # Write parameters
        self.writeParameters()

        # Update plot on startup
        self.updatePlot()

    def writeParameters(self):
        # Write paramters to PLC
        self.plc.write_by_name('MAIN.em1500.hydro.stInput.w0', self.spectrum.w0, pyads.PLCTYPE_LREAL)
        self.plc.write_by_name('MAIN.em1500.hydro.stInput.lambda', self.spectrum.Lambda, pyads.PLCTYPE_LREAL)
        self.plc.write_by_name('MAIN.em1500.hydro.stInput.sigma', self.spectrum.sigma, pyads.PLCTYPE_LREAL)

        self.plc.write_by_name('MAIN.em8000.hydro.stInput.w0', self.spectrum.w0, pyads.PLCTYPE_LREAL)
        self.plc.write_by_name('MAIN.em8000.hydro.stInput.lambda', self.spectrum.Lambda, pyads.PLCTYPE_LREAL)
        self.plc.write_by_name('MAIN.em8000.hydro.stInput.sigma', self.spectrum.sigma, pyads.PLCTYPE_LREAL)
        
    def updatePlot(self):
        f = self.spectrum.w/(2*np.pi)
        xMin = min(f)
        xMax = max(f)
        yMin = 0
        yMax = 1.1*max(max(self.spectrum.S), max(self.spectrum.Slin))

        self.spectrumPlot.plot.setXRange(xMin, xMax)
        self.spectrumPlot.plot.setYRange(yMin, yMax)

        
        self.spectrumPlot.static_plot(f,
            [
                self.spectrum.S,
                self.spectrum.Slin
            ]
        )


class E_SpectrumType(Enum):
    PMS = 0
    JONSWAP = 1
    

class WaveSpectrum(object):
    def __init__(self, Hs=2.5, Tp=12.0, spec=E_SpectrumType.JONSWAP):
        # Input parameters
        self.Hs = Hs
        self.Tp = Tp
        self.spec = spec

        # Calculated parameters
        self.w = []
        self.S = []
        self.Slin = []
        self.w0 = []
        self.sigma = []
        self.Lambda = []

        # Initial parameter calculation
        self.calculate(self.Hs, self.Tp, self.spec)

    def calculate(self, Hs, Tp, spec):
        # Inital frequency range
        N = 400
        w_min = 0.01
        # w_max = np.pi/2
        w_max = 2.5*1/Tp*2*np.pi
        
        self.w = np.linspace(w_min, w_max, N)
        self.S = np.zeros(N)            
        # Calculate wavespectrum
        if spec == E_SpectrumType.PMS:
            for k in range(0, N):
                # From average wave period to zero crossing period
                Tz = 0.921*Tp
                
                # PM constants
                A = 4*np.pi**3*Hs**2/(Tz**4)
                B = 16*np.pi**3/(Tz**4)
                
                # Calculate wave spectrum 
                self.S[k] = A/(self.w[k]**5)*np.exp(-B/(self.w[k]**4))
                
        elif spec == E_SpectrumType.JONSWAP:
            for k in range(0, N):
                if self.w[k] <= 5.24/Tp:
                    sigma = 0.07
                else:
                    sigma = 0.09
                    
                Y = np.exp(-((0.191*self.w[k]*Tp-1)/(np.sqrt(2)*sigma))**2)
                
                # Calculate wave spectrum
                self.S[k] = 155*Hs**2/(Tp**4*self.w[k]**5)*np.exp(-944/(Tp**4*self.w[k]**4))*3.3**Y
        
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