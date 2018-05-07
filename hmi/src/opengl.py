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

        # Feedback data
        self.txHmi = TxHmi()

        # Tool length to WEP
        self.dtool = 0.567

        # Calibration data
        self.calib = calib
        self.Tgq = np.reshape(self.calib['WORLD_TO_QTM']['H'], (4, 4))
        self.Tg1 = np.reshape(self.calib['WORLD_TO_EM8000']['H'], (4, 4))
        self.Tg2 = np.reshape(self.calib['WORLD_TO_EM1500']['H'], (4, 4))
        self.T1r = np.reshape(self.calib['EM8000_TO_COMAU']['H'], (4, 4))
        
        # Static Coordinate systems
        self.ground = CoordinatePlot(
            self.widget,
            np.identity(4)
        )
        self.ground.setCoordinateProperties(axWidth=3, axLength=1)

        self.qtm = CoordinatePlot(
            self.widget,
            self.Tgq
        )
        self.neutralEM8000 = CoordinatePlot(
            self.widget,
            self.Tg1
        )
        self.neutralEM1500 = CoordinatePlot(
            self.widget,
            self.Tg2
        )
        
        # Moving Coordinate systems
        self.bodyEM8000 = CoordinatePlot(self.widget)
        self.bodyEM1500 = CoordinatePlot(self.widget)
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
    
        # Measured wire and estimated wire
        self.wire = gl.GLLinePlotItem(
            pos = np.zeros([2,3]),
            color = pg.glColor('g'),
            width = 2.0
        )
        self.wireEstimated = gl.GLLinePlotItem(
            pos = np.zeros([2,3]),
            color = pg.glColor('w'),
            width = 2.0
        )
        self.widget.addItem(self.wire)
        self.widget.addItem(self.wireEstimated)

        self.markers = dict()
        for i in range(0, len(self.txHmi.qtm.markers)):
            self.markers[i] = CoordinatePlot(self.widget)
            self.markers[i].setCoordinateProperties(axWidth=2, axLength=0.2)

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
        Hg1 = Tg1.dot(Txyz(em8000.eta[0:3])).dot(Rxyz(em8000.eta[3:6]))  
        self.bodyEM8000.updateTransformation(Hg1)

        # EM8000
        Tg2 = np.reshape(calib['WORLD_TO_EM1500']['H'], (4, 4))
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

            # Hook position in {g}
            Pt = np.array([
                p2[0],
                p2[1],
                p2[2],
                1
            ])

            self.links[i].setData(
                pos = points
            )

            

        # Qtm markers
        if self.txHmi.qtm.status != -1:
            for i in range(0, len(self.markers)):
                # Tool point position

                # Hook position
                Ph = self.Tgq.dot(np.array([
                    self.txHmi.qtm.feedback.x,
                    self.txHmi.qtm.feedback.y,
                    self.txHmi.qtm.feedback.z,
                    1
                ]))


                # Set color based on detection mode
                if self.txHmi.qtm.feedback.status == 1:
                    color = pg.glColor('g')
                elif self.txHmi.qtm.feedback.status == 0:
                    color = pg.glColor('b')
                else:
                    color = pg.glColor('r')

                wirePoints = np.vstack((Pt[0:3], Ph[0:3]))
                self.wire.setData(
                    pos=wirePoints,
                    color=color
                )


                # Pm = np.array([
                #     self.txHmi.qtm.markers[i].x/1000.0,
                #     self.txHmi.qtm.markers[i].y/1000.0,
                #     self.txHmi.qtm.markers[i].z/1000.0,
                #     1
                # ])

                # Pm = self.Tgq.dot(Pm)

                # Tgm = np.identity(4)

                # Tgm[:,3] = Pm

                # self.markers[i].updateTransformation(Tgm)

        

        
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
    def __init__(self, glViewWidget, H0=np.identity(4)):
        self.widget = glViewWidget

        # Default parameters
        self.colors = [
            pg.glColor('r'),
            pg.glColor('g'),
            pg.glColor('b')
        ]
        self.axWidth = 2.0
        self.axLength = 0.5
        self.ax = dict()


        # Default location
        self.H = H0
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

    def setCoordinateProperties(self, axLength, axWidth):
        self.axLength = axLength
        self.axWidth = axWidth

        p0 = self.H[0:3,3]
        for i in range(0, 3):
            p1 = p0 + self.H[0:3,i]*self.axLength
            v = np.vstack((p0, p1))

            self.ax[i].setData(
                pos=v,
                width=self.axWidth
            )

            
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