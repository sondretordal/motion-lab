import time
import numpy as np
import matplotlib.pyplot as plt
from build import udp

s = udp.server(50060)

s.start()

time.sleep(1)

q1 = []
q2 = []
t = []
tS = time.time()
f = 1
while (time.time() - tS) <= 5.0:
    t.append((time.time() - tS)*1000.0)
    q = 10*np.sin(f*2*np.pi*t[-1]/1000.0)
    
    q1.append(q)
    
    s.Control.COMAU.q1 = q

    q2.append(s.Feedback.COMAU.q1)
        

    time.sleep(0.005)
    


plt.close()

plt.plot(t, q1)
plt.plot(t, q2)
plt.show()







