from build import MotionLab
import numpy as np
import time

ml = MotionLab.udpserver(50050)

ml.start()

#A = np.matrix(np.random.rand(500, 500))
#
#i = 1
#tS = time.time()
#
#while((time.time() - tS) <= 10.0):
#    B = A.I
#    i = i + 1

from build import MotionLab

ml.close()



