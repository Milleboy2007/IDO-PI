from bluedot.btcomm import BluetoothClient
from signal import pause
import busio
import board
import time

from adafruit_ads1x15.ads1115 import ADS1115
from adafruit_ads1x15.analog_in import AnalogIn

# Initialisation de l'interface i2c
i2c = busio.I2C(board.SCL, board.SDA)
 
# Créer une instance de la classe ADS1115 
# et l'associer à l'interface i2c
ads = ADS1115(i2c)
 
# Créer une instance d'entrée analogique
# et l'associer à la broche 0 du module ADC
data = AnalogIn(ads, 0)

def received(data):
    print(data)
 
SRV = "E4:5F:01:D6:2B:27"
# Lire la valeur numérique et le voltage
try:
    c = BluetoothClient(SRV, received)
    while True:
        print(data.value, data.voltage)
        time.sleep(1)
        c.send(str(data.value))

except KeyboardInterrupt:
    print("Programme interrompu.")