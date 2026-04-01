import socket

PORT = 8888
BUFFER_SIZE = 1024


# Créer le socket
socket_local = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
adr_local = ('', PORT)

# Lier le socket à l'adresse
socket_local.bind(adr_local)

print(f"On attend les messages UDP entrants au port {PORT}...")

# Réception des messages
while True:
    # Réception des données
    buffer, adr_dist = socket_local.recvfrom(BUFFER_SIZE)
    
    # Décodage binaire -> texte
    message = buffer.decode()

    print(f"Message reçu: {message}", end='')