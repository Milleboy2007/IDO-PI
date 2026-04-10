import pigpio
import time

pi = pigpio.pi()

TRIG = 5
ECHO = 6

def lecture_distance():
    # Déclenchement (Impulsion de 10µs)
    pi.write(TRIG, 1)
    time.sleep(0.00001)
    pi.write(TRIG, 0)

    start = time.time()
    stop = time.time()

    # Attente du début de l'écho
    while pi.read(ECHO) == 0:
        start = time.time()
    
    # Attente de la fin de l'écho
    while pi.read(ECHO) == 1:
        stop = time.time()

    duree = stop - start
    return round((duree * 34300) / 2, 1)

if __name__ == "__main__":
    print(lecture_distance())