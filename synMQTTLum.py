from bluedot.btcomm import BluetoothServer
from signal import pause
import paho.mqtt.client as pmc
import pigpio
 
BROKER = "10.10.2.26"
PORT = 1883
TOPIC = "exo"
 
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
    #print(donnees)
    luminosite = int(donnees)
 
 
try:
    # On instancie le serveur
    srv = BluetoothServer(reception)
 
    client = pmc.Client(pmc.CallbackAPIVersion.VERSION2)
    client.on_connect = connexion
    client.on_message = reception_msg
    client.username_pw_set("t","t")
 
    client.connect(BROKER,PORT)
 
    # Si je veux m'abonner je fais ceci
    client.subscribe(TOPIC)
 
    # Si je veux publier je fais ceci
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