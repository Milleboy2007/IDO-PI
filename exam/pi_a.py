from bluedot.btcomm import BluetoothClient
import pigpio
import time

pi = pigpio.pi()

SERVEUR = "E4:5F:01:EC:63:4A"
BTN_UP = 26
BTN_DOWN = 19
LEVEL = 3

pi.set_mode(BTN_UP, pigpio.INPUT)
pi.set_mode(BTN_DOWN, pigpio.INPUT)

def reception(data):
    print(data)

if __name__ == "__main__":
    try:
        c = BluetoothClient(SERVEUR, reception)
        prev_Up = -1
        prev_Down = -1
        while True:
            click_Up = pi.read(BTN_UP)
            if click_Up != prev_Up:
                isNew = True
                for i in range(LEVEL):
                    if pi.read(BTN_UP) != click_Up:
                        isNew = False
                        break
                    time.sleep(0.01)
                if isNew: 
                    prev_Up = click_Up
                    if click_Up == 0:
                        print("stock augmenter de 1")
                        c.send("INC")
            time.sleep(0.02)
            
            click_Down = pi.read(BTN_DOWN)
            if click_Down != prev_Down:
                isNew = True
                for i in range(LEVEL):
                    if pi.read(BTN_DOWN) != click_Down:
                        isNew = False
                        break
                    time.sleep(0.01)
                if isNew: 
                    prev_Down = click_Down
                    if click_Down == 0:
                        print("stock diminuer de 1")
                        c.send("DEC")
            time.sleep(0.02)
    except KeyboardInterrupt:
        pi.stop()