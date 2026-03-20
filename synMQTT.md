# Exo synthese pour MQTT

## Description
Un pi écoute une communication *BROKER* (sur un conteneur), afin de recevoire des ordre **ON**, **OFF**, **AUTO**. Il commnique également avec un deuxieme pi en bluetooth (pour le mode auto).

- **ON**: la lumière s'allume
- **OFF**: La lumière s'éteint
- **AUTO**: La lumière s'éteint ou s'allume par rapport a une luminosité envoyé par le pi B et avec un **seuil** de luminosité

## Conteneur
```cmd
mosquitto_sub -h 0.0.0.0 -u {Nom Utilisateur} -P {Mot de passe} -t {TOPIC}
mosquitto_pub -h 127.0.0.1 -u {Nom Utilisateur} -P {Mot de passe} -t {TOPIC} -m {Message a envoyer}
```

## Controlleur de lumière(PI A)
```python
from bluedot.btcomm import BluetoothServer
from signal import pause
import paho.mqtt.client as pmc
import pigpio
 
BROKER = "10.10.2.26" #--Addresse ip du conteneur
PORT = 1883           #--Port d'écoute de mosquitto sur le conteneur
TOPIC = "exo"         #--Topic d'écoute de mosquitto
 
LED = 26
SEUIL = 2000
 
pi = pigpio.pi()
 
 
global current_mode
current_mode = "OFF"

global luminosite
luminosite = 0
 
## fonctions mqtt
def connexion(client, userdata, flags, code, properties):
    if code == 0:
        print("Connecté")
    else:
        print("Erreur code %d\n", code)
 
def reception_msg(cl,userdata,msg):
    global current_mode
    print("Reçu:",msg.payload.decode())
    current_mode = msg.payload.decode()
 
 
# Fonction de rappel pour le traitement des messages entrants
def reception(donnees):
    global luminosite
    luminosite = int(donnees)
 
 
try:
    # On instancie le serveur
    srv = BluetoothServer(reception)
 
    client = pmc.Client(pmc.CallbackAPIVersion.VERSION2)
    client.on_connect = connexion
    client.on_message = reception_msg

    #(Nom utilisateur, mot de passe)
    client.username_pw_set("t","t")
 
    client.connect(BROKER,PORT)
 
    # Si je veux m'abonner je fais ceci
    client.subscribe(TOPIC)
 
    
    client.loop_start()
   
    while True:
        if current_mode == "AUTO":
            if luminosite > SEUIL:
                pi.write(LED,1)
            else:
                pi.write(LED,0)
        elif current_mode == "ON":
            pi.write(LED,1)
        elif current_mode == "OFF":
            pi.write(LED,0)
        else:
            print("Entrée invalide")
       
 
except KeyboardInterrupt:
    print("Programme interrompu")
    pi.write(LED,0)
```
## Capteur de lumière (PI B)
```python
from bluedot.btcomm import BluetoothClient
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
 
SRV = "E4:5F:01:D6:2B:27" #--Addresse mac du PI A

try:
    c = BluetoothClient(SRV, received)
    while True:
        print(data.value, data.voltage)
        time.sleep(1)
        c.send(str(data.value))

except KeyboardInterrupt:
    print("Programme interrompu.")
```