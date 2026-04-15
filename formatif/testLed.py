import pigpio
from time import sleep

pi = pigpio.pi()

R = 17
G = 27
B = 22

pi.set_mode(R, pigpio.OUTPUT)
pi.set_mode(G, pigpio.OUTPUT)
pi.set_mode(B, pigpio.OUTPUT)

pi.write(R, 1)
pi.write(G, 1)
pi.write(B, 1)

if __name__ == "__main__":
    try:
        while True:
            pi.write(R, 0)
            sleep(1)
            pi.write(R, 1)
            pi.write(G, 0)
            sleep(1)
            pi.write(G, 1)
            pi.write(B, 0)
            sleep(1)
            pi.write(B, 1)
    except KeyboardInterrupt:
        pi.write(R, 1)
        pi.write(G, 1)
        pi.write(B, 1)