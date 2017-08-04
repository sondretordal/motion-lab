import time
import numpy as np
import matplotlib.pyplot as plt
from build import udp

s = udp.server(50060)

s.start()

time.sleep(1)

s.close()







