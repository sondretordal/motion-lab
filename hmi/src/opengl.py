import numpy as np
from PyQt5 import QtCore
import pyqtgraph as pg
import pyqtgraph.opengl as gl

from src.math3d import Txyz, Rxyz, Rzyx, DH

from src.datastructures import TxHmi

class MotionLabVisualizer(QtCore.QObject):
    def __init__(self, calib, parent=None):
        # Construct super class
        super().__init__(parent)
        
        ## Private ##
        self.widget = gl.GLViewWidget()
        self.widget.addItem(gl.GLGridItem())

        # Tool length to WEP
        self.dtool = 0.567

        # Coordinate systems
        self.calib = calib
        self.bodyEM8000 = CoordinatePlot(self.widget)
        self.bodyMRU1 = CoordinatePlot(self.widget)
        self.neutralEM8000 = CoordinatePlot(self.widget)
        
        self.bodyEM1500 = CoordinatePlot(self.widget)
        self.bodyMRU2 = CoordinatePlot(self.widget)
        self.neutralEM1500 = CoordinatePlot(self.widget)

        self.baseCOMAU = CoordinatePlot(self.widget)
        self.jointsCOMAU = dict()
        self.links = dict()

        for i in range(0, 4):
            self.jointsCOMAU[i] = CoordinatePlot(self.widget)

            self.links[i] = gl.GLLinePlotItem(
                pos = np.zeros([2,3]),
                color = pg.glColor('w'),
                width = 2.0
            )

            # Add to widget
            self.widget.addItem(self.links[i])

        



        # Feedback data
        self.txHmi = TxHmi()

    # Public methods
    def setTxHmi(self, txHmi):
        assert type(txHmi) is TxHmi
        self.txHmi = txHmi

    def update(self):
        # Read data
        calib = self.calib
        em8000 = self.txHmi.em8000
        em1500 = self.txHmi.em1500
        comau = self.txHmi.comau
        winch = self.txHmi.winch

        # EM8000
        Tg1 = np.reshape(calib['WORLD_TO_EM8000']['H'], (4, 4))
        self.neutralEM8000.updateTransformation(Tg1)
        Hg1 = Tg1.dot(Txyz(em8000.eta[0:3])).dot(Rxyz(em8000.eta[3:6]))  
        self.bodyEM8000.updateTransformation(Hg1)

        # EM8000
        Tg2 = np.reshape(calib['WORLD_TO_EM1500']['H'], (4, 4))
        self.neutralEM1500.updateTransformation(Tg2)
        Hg2 = Tg2.dot(Txyz(em1500.eta[0:3])).dot(Rxyz(em1500.eta[3:6]))
        self.bodyEM1500.updateTransformation(Hg2)

        # COMAU
        Hgr = Hg1.dot(np.reshape(calib['EM8000_TO_COMAU']['H'], (4, 4)))
        self.baseCOMAU.updateTransformation(Hgr)

        # Forward kinematics
        T = self.forwardComauKinematics(comau.q)

        for i in range(0, len(self.links)):
            self.jointsCOMAU[i].updateTransformation(Hgr.dot(T[i]))

            if i == 0:
                H1 = Hgr
            else:
                H1 = Hgr.dot(T[i-1])

            H2 = Hgr.dot(T[i])

            p1 = H1[0:3,3]
            p2 = H2[0:3,3]

            points = np.vstack((p1, p2))


            self.links[i].setData(
                pos = points
            )

        
    def show(self):
        self.widget.show()
        self.widget.setGeometry(300, 200, 1000, 800)
        
        

    def isVisible(self):
        if self.widget.isVisible():
            return True
        else:
            return False

    # Private methods
    def forwardComauKinematics(self, q):
        # Static robot paramters
        a1 = 0.350
        a2 = 1.160
        a3 = 0.250
        d1 = 0.830
        d4 = 1.4922
        d6 = 0.210

        # Length to end of wire exit point
        L = d4 + d6 + self.dtool
    
        # Position {b} -> {t}
        q1 = q[0]
        q2 = q[1]
        q3 = q[2]
        
        T = dict()
        T[0] = DH(-q1, d1, a1, np.pi/2)
        T[1] = DH(np.pi/2 - q2, 0, a2, 0)
        T[2] = DH(q3 + np.pi/2 + q2, 0, a3, np.pi/2)
        T[3] = DH(np.pi, L, 0, 0)

        H = dict()
        H[0] = T[0]
        for i in range(1, len(T)):
            H[i] = H[i-1].dot(T[i])

        return H
        

    def pendulumKinematic(self, phi):
        pass

    
class CoordinatePlot(object):
    def __init__(self, glViewWidget):
        self.widget = glViewWidget

        self.colors = [
            pg.glColor('r'),
            pg.glColor('g'),
            pg.glColor('b')
        ]
        self.axWidth = 2.0
        self.axLength = 0.5
        self.ax = dict()


        # Default location
        self.H = np.identity(4)
        p0 = self.H[0:3,3]
        for i in range(0, 3):
            p1 = p0 + self.H[0:3,i]*self.axLength
            v = np.vstack((p0, p1))

            self.ax[i] = gl.GLLinePlotItem(
                pos=v,
                color=self.colors[i],
                width=self.axWidth
            )

            self.widget.addItem(self.ax[i])
            
    def updateTransformation(self, H):
        self.H = H
        p0 = self.H[0:3,3]
        for i in range(0, 3):
            p1 = p0 + self.H[0:3,i]*self.axLength
            v = np.vstack((p0, p1))

            self.ax[i].setData(
                pos=v,
                width=self.axWidth
            )