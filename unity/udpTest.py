
import socket
import time



s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.bind(('127.0.0.1', 1001))


while True:
    s.sendto(bytearray('abcd', 'utf-8'), ('127.0.0.1', 1000))

    # rxBuff = s.recv(1024)

    # print(rxBuff)

    time.sleep(1)


