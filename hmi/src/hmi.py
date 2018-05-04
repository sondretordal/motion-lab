from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import pyqtgraph as pg
import time
import pyads
import numpy as np
import ctypes
import json
from scipy.optimize import curve_fit

from src.classes import RealTimePlot, RealTimeBar, WaveSpectrum
from src.datastructures import TxHmi, RxHmi
from src.gui import Ui_main
from src.opengl import MotionLabVisualizer

# Motionlab pybind module
from lib import motionlab as ml


# Background color pyqtgraph
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')
pg.setConfigOptions(antialias=True)

class GUI(QMainWindow, Ui_main):
    def __init__(self):
        super(GUI, self).__init__()
        Ui_main.__init__(self)
        # Calling the initUI function
        self.initUI()

    # Function that initialize all the objects in the UI
    def initUI(self):
        # Set up the user interface from QT Designer
        self.setupUi(self)

        # Start ADS communications
        self.plc = pyads.Connection('192.168.90.150.1.1', 851)
        self.plc.open()

        self.tccom = pyads.Connection('192.168.90.150.1.1', 351)
        self.tccom.open()

        try:
            self.plc.read_state()
            self.plc_active = True

        except pyads.pyads.ADSError:
            self.plc_active = False

        try:
            self.tccom.read_state()
            self.tccom_active = True

        except pyads.pyads.ADSError:
            self.tccom_active = False


        # Xbox controller
        self.xbox = ml.XboxController()
        self.xbox.start()

        # Default function values
        self.waveSpectrumDP1 = WaveSpectrum()
        self.waveSpectrumDP2 = WaveSpectrum()

        # Setup of the different plots
        self.plot_setup()

        if self.plc_active:
            # Timer function for plot update
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_data)
            self.timer.start(50)

            self.EM8000_wave()
            self.EM1500_wave()

        # OpenGL
        text = open('./src/calib.json').read()
        calib = json.loads(text)
        self.visualizer = MotionLabVisualizer(calib)

        # Read inition time
        self.tStart = time.time()

        # Connect the interaction functionality of the GUI
        self.ui_connect()

        # Show UI
        self.show()

    def buttonAdsToggled(self, btn, adsVar):
        print('Toggled')
        

    # EM8000 Wave Settings
    def EM8000_wave(self):
            # Current wave spectrum data
            Hs = self.waveSpectrumDP1.Hs
            T1 = self.waveSpectrumDP1.T1
            spec = self.waveSpectrumDP1.spec

            try:
                objectName = self.sender().objectName()
                if objectName == "EM8000_wave_spectra":
                    spec = str(self.sender().currentText())

                elif objectName == "EM8000_wave_height":
                    Hs = int(self.sender().text())

                elif objectName == "EM8000_wave_period":
                    T1 = int(self.sender().text())
 
            except AttributeError:
                pass

            # Update wave spectrum and plot
            self.waveSpectrumDP1.calculate(Hs, T1, spec)

            self.DP1_spectrum.plot.setYRange(0, max(self.waveSpectrumDP1.S) + 5)
            self.DP1_spectrum.static_plot(self.waveSpectrumDP1.w,
                    [self.waveSpectrumDP1.S, self.waveSpectrumDP1.Slin]
                )
            
            # Write to TcCOM object containg WaveSimulator
            self.tccom.write_by_name('WaveSimulatorEM8000.ModelParameters.w0_Value', 
                    self.waveSpectrumDP1.w0, pyads.PLCTYPE_LREAL
                )

            self.tccom.write_by_name('WaveSimulatorEM8000.ModelParameters.sigma_Value', 
                    self.waveSpectrumDP1.sigma, pyads.PLCTYPE_LREAL
                )

            self.tccom.write_by_name('WaveSimulatorEM8000.ModelParameters.lambda_Value', 
                    self.waveSpectrumDP1.Lambda, pyads.PLCTYPE_LREAL
                )
        
            # EM8000 Wave Settings
    def EM1500_wave(self):
            # Current wave spectrum data
            Hs = self.waveSpectrumDP2.Hs
            T1 = self.waveSpectrumDP2.T1
            spec = self.waveSpectrumDP2.spec

            try:
                objectName = self.sender().objectName()
                if objectName == "EM1500_wave_spectra":
                    spec = str(self.sender().currentText())

                elif objectName == "EM1500_wave_height":
                    Hs = int(self.sender().text())

                elif objectName == "EM1500_wave_period":
                    T1 = int(self.sender().text())
 
            except AttributeError:
                pass

            # Update wave spectrum and plot
            self.waveSpectrumDP2.calculate(Hs, T1, spec)

            self.DP2_spectrum.plot.setYRange(0, max(self.waveSpectrumDP2.S) + 5)
            self.DP2_spectrum.static_plot(self.waveSpectrumDP2.w,
                    [self.waveSpectrumDP2.S, self.waveSpectrumDP2.Slin]
                )
            
            # Write to TcCOM object containg WaveSimulator
            self.tccom.write_by_name('WaveSimulatorEM1500.ModelParameters.w0_Value', 
                    self.waveSpectrumDP2.w0, pyads.PLCTYPE_LREAL
                )

            self.tccom.write_by_name('WaveSimulatorEM1500.ModelParameters.sigma_Value', 
                    self.waveSpectrumDP2.sigma, pyads.PLCTYPE_LREAL
                )

            self.tccom.write_by_name('WaveSimulatorEM1500.ModelParameters.lambda_Value', 
                    self.waveSpectrumDP2.Lambda, pyads.PLCTYPE_LREAL
                )

    # Plot setup
    def plot_setup(self):

        # Plot time range setting
        self.time_range = 20

        # Signal comparator tab:
        #------------------------------------------------------#
        self.signalDebugger = RealTimePlot(self.singalDebugWidget.addPlot())
        self.signalDebugger.plot.setLabel('left', 'Values ')
        self.signalDebugger.add_curves(['r', 'b'], ['Signal 1', 'Signal 2'])

        # Ship Simulator tab:
        #------------------------------------------------------#

        # EM8000
        self.DP1_1 = RealTimePlot(self.DP1_SimStates.addPlot())
        self.DP1_1.plot.setLabel('left', 'Position', 'm')
        self.DP1_1.plot.setYRange(-0.5, 0.5)
        self.DP1_1.add_curves(['r', 'g', 'b'], ['Surge', 'Sway', 'Heave'])
        self.DP1_SimStates.nextRow()
        self.DP1_2 = RealTimePlot(self.DP1_SimStates.addPlot())
        self.DP1_2.plot.setLabel('left', 'Angle', 'deg')
        self.DP1_2.plot.setYRange(-6.0, 6.0)
        self.DP1_2.add_curves(['r', 'g', 'b'], ['Roll', 'Pitch', 'Yaw'])

        self.DP1_spectrum = RealTimePlot(self.DP1_wavespectrum.addPlot())
        self.DP1_spectrum.plot.setLabel('left', 'Spectrum Energy', '-')
        self.DP1_spectrum.plot.setLabel('bottom', 'Wave Period', 'rad/s')
        self.DP1_spectrum.plot.setYRange(0, 30)
        self.DP1_spectrum.add_curves(['r','b'], ['Wave Spectrum', 'Linear Spectrum'])

        # EM1500
        self.DP2_1 = RealTimePlot(self.DP2_SimStates.addPlot())
        self.DP2_1.plot.setLabel('left', 'Position', 'm')
        self.DP2_1.plot.setYRange(-0.5, 0.5)
        self.DP2_1.add_curves(['r', 'g', 'b'], ['Surge', 'Sway', 'Heave'])
        self.DP2_SimStates.nextRow()
        self.DP2_2 = RealTimePlot(self.DP2_SimStates.addPlot())
        self.DP2_2.plot.setLabel('left', 'Angle', 'deg')
        self.DP2_2.plot.setYRange(-6.0, 6.0)
        self.DP2_2.add_curves(['r', 'g', 'b'], ['Roll', 'Pitch', 'Yaw'])

        self.DP2_spectrum = RealTimePlot(self.DP2_wavespectrum.addPlot())
        self.DP2_spectrum.plot.setLabel('left', 'Spectrum Energy', '-')
        self.DP2_spectrum.plot.setLabel('bottom', 'Wave Period', 'rad/s')
        self.DP2_spectrum.plot.setYRange(0, 15)
        self.DP2_spectrum.add_curves(['r','b'], ['Wave Spectrum', 'Linear Spectrum'])

        # Plot tab
        #------------------------------------------------------#
        self.EM1500_1 = RealTimePlot(self.EM1500_plot.addPlot())
        self.EM1500_1.plot.setYRange(-0.5, 0.5)
        self.EM1500_1.plot.setLabel('left', 'Position', 'm')
        self.EM1500_1.add_curves(['r', 'g', 'b'], ['Surge', 'Sway', 'Heave'])
        self.EM1500_1.add_text_displays([
                self.EM1500_output_pos_x, 
                self.EM1500_output_pos_y, 
                self.EM1500_output_pos_z
            ])
        self.EM1500_plot.nextRow()
        self.EM1500_2 = RealTimePlot(self.EM1500_plot.addPlot())
        self.EM1500_2.plot.setYRange(-5, 5)
        self.EM1500_2.plot.setLabel('left', 'Angle', 'deg')
        self.EM1500_2.add_curves(['r', 'g', 'b'], ['Roll', 'Pitch', 'Yaw'])
        self.EM1500_2.add_text_displays([
                self.EM1500_output_ang_r, 
                self.EM1500_output_ang_p, 
                self.EM1500_output_ang_y
            ])
        
        self.EM8000_1 = RealTimePlot(self.EM8000_plot.addPlot())
        self.EM8000_1.plot.setYRange(-1, 1)
        self.EM8000_1.plot.setLabel('left', 'Position', 'm')
        self.EM8000_1.add_curves(['r', 'g', 'b'], ['Surge', 'Sway', 'Heave'])
        self.EM8000_1.add_text_displays([
                self.EM8000_output_pos_x, 
                self.EM8000_output_pos_y, 
                self.EM8000_output_pos_z
            ])
        self.EM8000_plot.nextRow()
        self.EM8000_2 = RealTimePlot(self.EM8000_plot.addPlot())
        self.EM8000_2.plot.setLabel('left', 'Angle', 'deg')
        self.EM8000_2.plot.setYRange(-5, 5)
        self.EM8000_2.add_curves(['r', 'g', 'b'], ['Roll', 'Pitch', 'Yaw'])
        self.EM8000_2.add_text_displays([
                self.EM8000_output_ang_r, 
                self.EM8000_output_ang_p, 
                self.EM8000_output_ang_y
            ])

        self.COMAU = RealTimePlot(self.COMAU_plot.addPlot())
        self.COMAU.plot.setYRange(-180, 180)
        self.COMAU.plot.setLabel('left', 'Angle', 'deg')
        self.COMAU.add_curves(['r', 'g', 'b', 'y', 'm', 'c'], ['q1', 'q2', 'q3', 'q4', 'q5', 'q6'])
        self.COMAU.add_text_displays([
                self.COMAU_output_pos_j1, 
                self.COMAU_output_pos_j2, 
                self.COMAU_output_pos_j3,
                self.COMAU_output_pos_j4, 
                self.COMAU_output_pos_j5, 
                self.COMAU_output_pos_j6
            ])

        # Joint stroke bar indicators
        self.EM1500_bars = RealTimeBar()
        self.EM1500_bars.max_values = [0.395]*12
        self.EM1500_bars.bars = [
                self.EM1500_bar1_l1, 
                self.EM1500_bar1_l2, 
                self.EM1500_bar1_l3, 
                self.EM1500_bar1_l4, 
                self.EM1500_bar1_l5, 
                self.EM1500_bar1_l6,
                self.EM1500_bar2_l1, 
                self.EM1500_bar2_l2, 
                self.EM1500_bar2_l3, 
                self.EM1500_bar2_l4, 
                self.EM1500_bar2_l5, 
                self.EM1500_bar2_l6
            ]
        
        self.EM8000_bars = RealTimeBar()
        self.EM8000_bars.max_values = [0.776]*12
        self.EM8000_bars.bars = [
                self.EM8000_bar1_l1, 
                self.EM8000_bar1_l2, 
                self.EM8000_bar1_l3, 
                self.EM8000_bar1_l4, 
                self.EM8000_bar1_l5, 
                self.EM8000_bar1_l6,
                self.EM8000_bar2_l1, 
                self.EM8000_bar2_l2, 
                self.EM8000_bar2_l3, 
                self.EM8000_bar2_l4, 
                self.EM8000_bar2_l5, 
                self.EM8000_bar2_l6
            ]
        
        self.COMAU_bars = RealTimeBar()
        self.COMAU_bars.max_values = [180]*12
        self.COMAU_bars.bars = [
                self.COMAU_bar1_j1, 
                self.COMAU_bar1_j2, 
                self.COMAU_bar1_j3,
                self.COMAU_bar1_j4, 
                self.COMAU_bar1_j5, 
                self.COMAU_bar1_j6,
                self.COMAU_bar2_j1, 
                self.COMAU_bar2_j2, 
                self.COMAU_bar2_j3, 
                self.COMAU_bar2_j4, 
                self.COMAU_bar2_j5, 
                self.COMAU_bar2_j6
            ]

        # Xbox controller
        self.XBOX_bars = RealTimeBar()
        self.XBOX_bars.max_values = [1.0]*4
        self.XBOX_bars.bars = [
                self.XboxJoystickLeft_x,
                self.XboxJoystickLeft_y,
                self.XboxJoystickRight_x,
                self.XboxJoystickRight_y,
            ]

    
    # UI connections
    def ui_connect(self):


        # Signal compare tab
        self.autoScale.clicked.connect(self.auto_scale)
        self.time_range_signalDebugger.currentIndexChanged.connect(self.plot_time_axis_range)

        # Interface Tab:
        #----------------------------------------------------------#
        # Connecting EM 8000 Interface-buttons to functions
        self.EM8000_settled_btn.clicked.connect(self.EM8000_settled)
        self.EM8000_neutral_btn.clicked.connect(self.EM8000_neutral)
        self.EM8000_engaged_btn.clicked.connect(self.EM8000_engaged)

        # Connecting EM 1500 Interface-buttons to functions
        self.EM1500_settled_btn.clicked.connect(self.EM1500_settled)
        self.EM1500_neutral_btn.clicked.connect(self.EM1500_neutral)
        self.EM1500_engaged_btn.clicked.connect(self.EM1500_engaged)

        # Connecting COMAU Interface-buttons to functions
        self.COMAU_settled_btn.clicked.connect(self.COMAU_settled)
        self.COMAU_engaged_btn.clicked.connect(self.COMAU_engaged)
        self.COMAU_engaged_fast_btn.clicked.connect(self.COMAU_engaged_fast)

        # Connecting SYSTEM Interface-buttons to functions
        self.SYSTEM_settled_btn.clicked.connect(self.SYSTEM_settled)
        self.SYSTEM_stop_btn.clicked.connect(self.SYSTEM_stop)

        # Plotting Tab:
        #----------------------------------------------------------#
        self.EM1500_plot_time_range.currentIndexChanged.connect(self.plot_time_axis_range)
        self.EM8000_plot_time_range.currentIndexChanged.connect(self.plot_time_axis_range)
        self.COMAU_plot_time_range.currentIndexChanged.connect(self.plot_time_axis_range)

        # Ship Simulator tab:
        #----------------------------------------------------------#
        self.EM1500_plot_time_range_ship.currentIndexChanged.connect(self.plot_time_axis_range)
        self.EM8000_plot_time_range_ship.currentIndexChanged.connect(self.plot_time_axis_range)

        # Limit values for input
        self.validator_height = QIntValidator(1, 10)
        self.validator_period = QIntValidator(1, 20)

        self.EM8000_wave_height.setText(str(self.waveSpectrumDP1.Hs))
        self.EM8000_wave_height.setValidator(self.validator_height)

        self.EM8000_wave_period.setText(str(self.waveSpectrumDP1.T1))
        self.EM8000_wave_period.setValidator(self.validator_period)

        self.EM8000_wave_height.returnPressed.connect(self.EM8000_wave)
        self.EM8000_wave_period.returnPressed.connect(self.EM8000_wave)
        self.EM8000_wave_spectra.currentIndexChanged.connect(self.EM8000_wave)


        self.EM1500_wave_height.setText(str(self.waveSpectrumDP2.Hs))
        self.EM1500_wave_height.setValidator(self.validator_height)

        self.EM1500_wave_period.setText(str(self.waveSpectrumDP2.T1))
        self.EM1500_wave_period.setValidator(self.validator_period)
        
        self.EM1500_wave_height.returnPressed.connect(self.EM1500_wave)
        self.EM1500_wave_period.returnPressed.connect(self.EM1500_wave)
        self.EM1500_wave_spectra.currentIndexChanged.connect(self.EM1500_wave)

        # Winch related
        self.winchSettled.clicked.connect(lambda: self.plc.write_by_name('MAIN.winch.mode', 0, pyads.PLCTYPE_UINT))
        self.winchEngaged.clicked.connect(lambda: self.plc.write_by_name('MAIN.winch.mode', 1, pyads.PLCTYPE_UINT))
        self.winchEngagedFast.clicked.connect(lambda: self.plc.write_by_name('MAIN.winch.mode', 2, pyads.PLCTYPE_UINT))

        self.winchOff.clicked.connect(lambda: self.plc.write_by_name('MAIN.winch.enable', False, pyads.PLCTYPE_BOOL))
        self.winchOn.clicked.connect(lambda: self.plc.write_by_name('MAIN.winch.enable', True, pyads.PLCTYPE_BOOL))
        self.winchReset.clicked.connect(lambda: self.plc.write_by_name('MAIN.winch.reset', True, pyads.PLCTYPE_BOOL))
        self.winchStopp.clicked.connect(lambda: self.plc.write_by_name('MAIN.winch.stopp', True, pyads.PLCTYPE_BOOL))

        # Show 3D visulaization of motion-lab
        self.show3dView.clicked.connect(self.visualizer.show)

    def test(self):
        print('Pushed')

    # Update data and plot
    def update_data(self):
        # Update HMI data
        txHmi = self.plc.read_by_name('MAIN.txHmi', TxHmi)

        rxHmi = RxHmi()

        rxHmi.xboxLeftX = self.xbox.left.x
        rxHmi.xboxLeftY = self.xbox.left.y
        rxHmi.xboxRightX = self.xbox.right.x
        rxHmi.xboxRightY = self.xbox.right.y
        rxHmi.xboxLT = self.xbox.LT
        rxHmi.xboxRT = self.xbox.RT

        # Update visualizer data
        self.visualizer.setTxHmi(txHmi)

        if self.visualizer.isVisible():
            self.visualizer.update()
            

        # Update activity boxes
        if txHmi.em8000.status == -1:
            self.activeEM8000.setCheckState(False)
        else:
            self.activeEM8000.setCheckState(True)
        
        if txHmi.em1500.status == -1:
            self.activeEM1500.setCheckState(False)
        else:
            self.activeEM1500.setCheckState(True)

        if txHmi.comau.status == -1:
            self.activeCOMAU.setCheckState(False)
        else:
            self.activeCOMAU.setCheckState(True)
        
        rxBuffer = bytearray(rxHmi)
        rxSize = len(rxBuffer)*pyads.PLCTYPE_BYTE
        self.plc.write_by_name('MAIN.rxHmi', rxBuffer, rxSize)
        
        self.t = time.time() - self.tStart
    
        self.DP1_1.time_range = self.time_range
        self.DP1_1.update(self.t, [
                txHmi.em8000.eta_sim[0],
                txHmi.em8000.eta_sim[1],
                txHmi.em8000.eta_sim[2]
            ])
        
        self.DP1_2.time_range = self.time_range
        self.DP1_2.update(self.t, [
                txHmi.em8000.eta_sim[3]/np.pi*180.0,
                txHmi.em8000.eta_sim[4]/np.pi*180.0,
                txHmi.em8000.eta_sim[5]/np.pi*180.0
            ])
 
        self.DP2_1.time_range = self.time_range
        self.DP2_1.update(self.t, [
                txHmi.em1500.eta_sim[0],
                txHmi.em1500.eta_sim[1],
                txHmi.em1500.eta_sim[2]
            ])
        
        self.DP2_2.time_range = self.time_range
        self.DP2_2.update(self.t, [
                txHmi.em1500.eta_sim[3]/np.pi*180.0,
                txHmi.em1500.eta_sim[4]/np.pi*180.0,
                txHmi.em1500.eta_sim[5]/np.pi*180.0
            ])

        self.EM1500_1.time_range = self.time_range
        self.EM1500_1.update(self.t, [
                txHmi.em1500.eta[0],
                txHmi.em1500.eta[1],
                txHmi.em1500.eta[2]
            ])
        self.EM1500_2.time_range = self.time_range
        self.EM1500_2.update(self.t, [
                txHmi.em1500.eta[3]/np.pi*180.0,
                txHmi.em1500.eta[4]/np.pi*180.0,
                txHmi.em1500.eta[5]/np.pi*180.0
            ])

        self.EM8000_1.time_range = self.time_range
        self.EM8000_1.update(self.t, [
                txHmi.em8000.eta[0],
                txHmi.em8000.eta[1],
                txHmi.em8000.eta[2]
            ])
        self.EM8000_2.time_range = self.time_range
        self.EM8000_2.update(self.t, [
                txHmi.em8000.eta[3]/np.pi*180.0,
                txHmi.em8000.eta[4]/np.pi*180.0,
                txHmi.em8000.eta[5]/np.pi*180.0
            ])
        
        self.COMAU.time_range = self.time_range
        self.COMAU.update(self.t, [
                txHmi.comau.q[0]/np.pi*180.0, 
                txHmi.comau.q[1]/np.pi*180.0, 
                txHmi.comau.q[2]/np.pi*180.0,
                txHmi.comau.q[3]/np.pi*180.0, 
                txHmi.comau.q[4]/np.pi*180.0, 
                txHmi.comau.q[5]/np.pi*180.0
            ])
        
        self.EM8000_bars.update([
                txHmi.em8000.cyl[0], 
                txHmi.em8000.cyl[1], 
                txHmi.em8000.cyl[2],
                txHmi.em8000.cyl[3], 
                txHmi.em8000.cyl[4], 
                txHmi.em8000.cyl[5],
                txHmi.em8000.cyl[0], 
                txHmi.em8000.cyl[1], 
                txHmi.em8000.cyl[2],
                txHmi.em8000.cyl[3], 
                txHmi.em8000.cyl[4], 
                txHmi.em8000.cyl[5]
            ])

        self.EM1500_bars.update([
                txHmi.em1500.cyl[0], 
                txHmi.em1500.cyl[1], 
                txHmi.em1500.cyl[2],
                txHmi.em1500.cyl[3], 
                txHmi.em1500.cyl[4], 
                txHmi.em1500.cyl[5],
                txHmi.em1500.cyl[0], 
                txHmi.em1500.cyl[1], 
                txHmi.em1500.cyl[2],
                txHmi.em1500.cyl[3], 
                txHmi.em1500.cyl[4], 
                txHmi.em1500.cyl[5]
            ])

        self.COMAU_bars.update([
                txHmi.comau.q[0]/np.pi*180.0, 
                txHmi.comau.q[1]/np.pi*180.0, 
                txHmi.comau.q[2]/np.pi*180.0,
                txHmi.comau.q[3]/np.pi*180.0, 
                txHmi.comau.q[4]/np.pi*180.0, 
                txHmi.comau.q[5]/np.pi*180.0,
                txHmi.comau.q[0]/np.pi*180.0, 
                txHmi.comau.q[1]/np.pi*180.0, 
                txHmi.comau.q[2]/np.pi*180.0,
                txHmi.comau.q[3]/np.pi*180.0, 
                txHmi.comau.q[4]/np.pi*180.0, 
                txHmi.comau.q[5]/np.pi*180.0
            ])

        # Xbox data
        self.XBOX_bars.update([
                self.xbox.left.x,
                self.xbox.left.y,
                self.xbox.right.x,
                self.xbox.right.y
            ])

        # Signal comparator
        if self.tabWidget.currentIndex() == 6:
            
            try:
                signal1 = self.plc.read_by_name(self.textSignal_1.toPlainText(), pyads.PLCTYPE_REAL)
            except pyads.pyads.ADSError:
                signal1 = 0.0

            try:
                signal2 = self.plc.read_by_name(self.textSignal_2.toPlainText(), pyads.PLCTYPE_REAL)
            except pyads.pyads.ADSError:
                signal2 = 0.0
    
            # Update data
            self.signalDebugger.time_range = self.time_range
            self.signalDebugger.update(self.t, [
                        signal1,
                        signal2
                    ])
            
    def auto_scale(self):
        t = self.signalDebugger.time
        loc = np.argmin(np.abs(t - (t[-1] - self.signalDebugger.time_range)))
        n = len(t) - loc

        max_values = [0.0, 0.0]
        min_values = [0.0, 0.0]

        for i in range(0, len(max_values)):
            max_values[i] = np.max(self.signalDebugger.data[i][-n:])
            min_values[i] = np.min(self.signalDebugger.data[i][-n:])
        
        new_range = [np.min(min_values), np.max(max_values)]

        if (new_range[0] != 0.0) and (new_range[1] != 0.0):
            self.signalDebugger.plot.setYRange(new_range[0], new_range[1])


    # Function to change the time axis range of the plots
    def plot_time_axis_range(self):
        # (This function is universal for all combobox objects in the plot tabs)

        # Set the time_range equal to combobox-object text
        self.time_range = int(self.sender().currentText())

        # Find and set the selected index to all combobox objects in the plot tabs
        val = self.sender().currentIndex()
        
        # Plotting tab:
        self.EM8000_plot_time_range.setCurrentIndex(val)
        self.EM1500_plot_time_range.setCurrentIndex(val)
        self.COMAU_plot_time_range.setCurrentIndex(val)

        # Ship Simulator tab:
        self.EM8000_plot_time_range_ship.setCurrentIndex(val)
        self.EM1500_plot_time_range_ship.setCurrentIndex(val)


    # EM 8000 button functions
    def EM8000_settled(self):
        self.EM8000_settled_btn.setStyleSheet("background-color: #cccccc")
        self.EM8000_neutral_btn.setStyleSheet("background-color: none   ")
        self.EM8000_engaged_btn.setStyleSheet("background-color: none   ")

        # Write to PLC: EM8000 settled = 1
        self.plc.write_by_name('MAIN.em8000.cmnd', 1, pyads.PLCTYPE_DINT)

    def EM8000_neutral(self):
        self.EM8000_settled_btn.setStyleSheet("background-color: none   ")
        self.EM8000_neutral_btn.setStyleSheet("background-color: #cccccc")
        self.EM8000_engaged_btn.setStyleSheet("background-color: none   ")

        # Write to PLC: EM8000 neutral = 3
        self.plc.write_by_name('MAIN.em8000.cmnd', 3, pyads.PLCTYPE_DINT)

    def EM8000_engaged(self):
        self.EM8000_settled_btn.setStyleSheet("background-color: none   ")
        self.EM8000_neutral_btn.setStyleSheet("background-color: none   ")
        self.EM8000_engaged_btn.setStyleSheet("background-color: #cccccc")

        # Write to PLC: EM8000 engaged = 7
        self.plc.write_by_name('MAIN.em8000.cmnd', 7, pyads.PLCTYPE_DINT)

    # EM 1500 button functions
    def EM1500_settled(self):
        self.EM1500_settled_btn.setStyleSheet("background-color: #cccccc")
        self.EM1500_neutral_btn.setStyleSheet("background-color: none")
        self.EM1500_engaged_btn.setStyleSheet("background-color: none")

        # Write to PLC: EM1500 settled = 1
        self.plc.write_by_name('MAIN.em1500.cmnd', 1, pyads.PLCTYPE_DINT)

    def EM1500_neutral(self):
        self.EM1500_settled_btn.setStyleSheet("background-color: none   ")
        self.EM1500_neutral_btn.setStyleSheet("background-color: #cccccc")
        self.EM1500_engaged_btn.setStyleSheet("background-color: none   ")

        # Write to PLC: EM1500 neutral = 3
        self.plc.write_by_name('MAIN.em1500.cmnd', 3, pyads.PLCTYPE_DINT)

    def EM1500_engaged(self):
        self.EM1500_settled_btn.setStyleSheet("background-color: none   ")
        self.EM1500_neutral_btn.setStyleSheet("background-color: none   ")
        self.EM1500_engaged_btn.setStyleSheet("background-color: #cccccc")

        # Write to PLC: EM1500 engaged = 7
        self.plc.write_by_name('MAIN.em1500.cmnd', 7, pyads.PLCTYPE_DINT)

    # COMAU button functions
    def COMAU_settled(self):
        self.COMAU_settled_btn.setStyleSheet("background-color: #cccccc")
        self.COMAU_engaged_btn.setStyleSheet("background-color: none   ")
        self.COMAU_engaged_fast_btn.setStyleSheet("background-color: none")

        # Write to PLC: COMAU settled = 1
        self.plc.write_by_name('MAIN.comau.cmnd', 0, pyads.PLCTYPE_DINT)

    def COMAU_engaged(self):
        self.COMAU_settled_btn.setStyleSheet("background-color: none   ")
        self.COMAU_engaged_btn.setStyleSheet("background-color: #cccccc")
        self.COMAU_engaged_fast_btn.setStyleSheet("background-color: none")

        # Write to PLC: COMAU engaged = 1
        self.plc.write_by_name('MAIN.comau.cmnd', 1, pyads.PLCTYPE_DINT)

    def COMAU_engaged_fast(self):
        self.COMAU_settled_btn.setStyleSheet("background-color: none")
        self.COMAU_engaged_btn.setStyleSheet("background-color: none")
        self.COMAU_engaged_fast_btn.setStyleSheet("background-color: #cccccc")

        # Write to PLC: COMAU engaged-fast = 2
        self.plc.write_by_name('MAIN.comau.cmnd', 2, pyads.PLCTYPE_DINT)

    # SYSTEM button functions
    def SYSTEM_settled(self):
        self.SYSTEM_settled_btn.setStyleSheet("background-color: #cccccc")
        self.EM8000_settled()
        self.EM1500_settled()
        self.COMAU_settled()

    def SYSTEM_stop(self):
        self.SYSTEM_settled_btn.setStyleSheet("background-color: none")
        self.EM8000_settled()
        self.EM1500_settled()
        self.COMAU_settled()

    # Stop all function
    def stop_all(self):

        self.SYSTEM_stop()
        print('APPLICATION STOPPED')

    # Function to handle the closing event of to the application
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes |
        QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.stop_all()
            
            # Stop timed data read
            self.timer.stop()

            if self.plc_active:
                # # Close ADS ports
                self.plc.close()
                self.tccom.close()
                print('Beckhoff ADS Connection Closed')

            # Stop xbox thread
            self.xbox.close()

            event.accept()
        else:
            event.ignore()
            
           