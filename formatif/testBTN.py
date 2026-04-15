import pigpio

pi = pigpio.pi()

BTN = 26

pi.set_mode(BTN, pigpio.INPUT)

if __name__ == "__main__":
    while True:
        print(pi.read(BTN))