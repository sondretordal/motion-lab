import time

from build import udp
# s = udp.server(50060)

s = udp.client(12345, '192.168.90.50')


tS = time.time()

t = []
i = 1
while time.time() - tS <= 5.0:
    s.update(i)
    i = i + 1
    time.sleep(0.01)



print len(t)





