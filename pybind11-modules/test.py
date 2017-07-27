from build import udp
import time

s = udp.server(50060,296,4)

s.start()
time.sleep(1)

ret = s.recv()

time.sleep(2)

print ret

s.close()






