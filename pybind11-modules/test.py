from build import MotionLab

import time

ml1 = MotionLab.udpserver(50060)
ml2 = MotionLab.udpserver(50160)

ml1.start()
ml2.start()




tS = time.time()
while((time.time() - tS) <= 5.0):
   print ml1.recv_data()


ml1.close()
ml2.close()



