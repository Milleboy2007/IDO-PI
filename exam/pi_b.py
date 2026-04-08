import paho.mqtt.client as pmc
from bluedot.btcomm import BluetoothServer
import pigpio

pi = pigpio.pi()

R = 19
G = 26
B = 13

BROKER = "10.10.2.26"
PORT = 1883
TOPIC = "entrepot/stock/commande"

stock = 0

pi.set_mode(R, pigpio.OUTPUT)
pi.set_mode(G, pigpio.OUTPUT)
pi.set_mode(B, pigpio.OUTPUT)
pi.write(B, 1) # led blue éteint par sureté puisqu'elle n'est pas utiliser

def reception_bluetooth(donnees):
    global stock
    # donnees upper afin d'assurer a 100% qu'elle soit dans le bon format
    if donnees.upper() == "INC":
        stock += 1
        print(f"Stock {donnees} de 1\nMaintenant a {stock}\n--------")
    elif donnees.upper() == "DEC":
        if stock != 0:
            stock -= 1
            print(f"Stock {donnees} de 1\nMaintenant a {stock}\n--------")
        else:
            print("Stock déja a 0\n--------")


def connexion_mqtt(client, userdata, flags, code, properties):
    if code == 0:
        print("Serveur MQTT connecté\n--------")
    else:
        print("Erreur code %d\n", code)

def reception_msg_mqtt(cl,userdata,msg):
    global stock
    order = msg.payload.decode()
    # order upper afin d'assurer a 100% qu'elle soit dans le bon format
    if order.upper() == "RESET":
        stock = 0
        print(f"Stock réinisialiser désormais a {stock}\n--------")
    else:
        try:
            order = int(order)
            if order >= 0:
                stock = order
                print(f"Stock désormais a {stock}\n--------")
            else:
                print(f"Valeur invalide stock reste inchanger a {stock}\n--------")
        except ValueError:
            print(f"Valeur invalide stock reste inchanger a {stock}\n--------")

client_mqtt = pmc.Client(pmc.CallbackAPIVersion.VERSION2)
client_mqtt.on_connect = connexion_mqtt
client_mqtt.on_message = reception_msg_mqtt

if __name__ == "__main__":
    try:
        client_mqtt.username_pw_set("exam", "2")
        client_mqtt.connect(BROKER,PORT)
        client_mqtt.subscribe(TOPIC)
        client_mqtt.loop_start()

        # On instancie le serveur
        srv_bluetooth = BluetoothServer(reception_bluetooth)

        while True:
            if stock == 0:
                pi.write(R, 0)
                pi.write(G, 1)
            else:
                pi.write(R, 1)
                pi.write(G, 0)
    except KeyboardInterrupt:
        pi.write(R, 1)
        pi.write(G, 1)
        pi.stop()