from bluedot.btcomm import BluetoothClient
from signal import pause
# L'adresse MAC du serveur
SERVEUR = "E4:5F:01:D6:2B:27"

def reception(data):
    print(data)

c = BluetoothClient(SERVEUR, reception)
c.send("bonjour")

pause()