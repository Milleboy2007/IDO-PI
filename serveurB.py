from bluedot.btcomm import BluetoothServer
from signal import pause

# Fonction de rappel pour le traitement des messages entrants
def reception(donnees):
    print(donnees)

# On instancie le serveur
srv = BluetoothServer(reception)

pause()