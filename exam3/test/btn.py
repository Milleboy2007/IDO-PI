import pigpio

pi = pigpio.pi()

BTN = 26

pi.set_mode(BTN, pigpio.INPUT)

while True:
    print(pi.read(BTN))