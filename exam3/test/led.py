import pigpio
import time

pi = pigpio.pi()

R1 = 22
B1 = 17
G1 = 27


R2 = 6
B2 = 5
G2 = 16

pi.set_mode(R1, pigpio.OUTPUT)
pi.set_mode(B1, pigpio.OUTPUT)
pi.set_mode(G1, pigpio.OUTPUT)

pi.set_mode(R2, pigpio.OUTPUT)
pi.set_mode(B2, pigpio.OUTPUT)
pi.set_mode(G2, pigpio.OUTPUT)

pi.write(R1, 1)
pi.write(B1, 1)
pi.write(G1, 1)

pi.write(R2, 1)
pi.write(B2, 1)
pi.write(G2, 1)

while True:
    pi.write(R1, 1)
    pi.write(B1, 1)
    pi.write(G1, 1)

    pi.write(R2, 1)
    pi.write(B2, 1)
    pi.write(G2, 1)
    time.sleep(1)
    pi.write(R1, 0)
    pi.write(B1, 0)
    pi.write(G1, 0)

    pi.write(R2, 0)
    pi.write(B2, 0)
    pi.write(G2, 0)
    time.sleep(1)