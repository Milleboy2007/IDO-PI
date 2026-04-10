from flask import Flask, jsonify, request
import socket
from datetime import datetime
import pigpio
from flask_cors import CORS
import time

RED = 17
BLUE = 27
GREEN = 22

TRIG = 5
ECHO = 6

seuil = 0

app = Flask(__name__)
CORS(app)

pi = pigpio.pi()

pi.set_mode(RED,pigpio.OUTPUT)
pi.set_mode(GREEN,pigpio.OUTPUT)
pi.set_mode(BLUE,pigpio.OUTPUT)

@app.route('/set_threshold', methods=['POST'])
def maj_seuil():
    global seuil
    print("SEUIL MAJ")
    seuil = request.get_json()['threshold']

@app.route('/get_distance', methods=['GET'])
def get_distance():
    print("DISTANCE ENVOYER")
    d = {}
    d['distance'] = lecture_distance()
    maj_led(d['distance'])
    return jsonify(d)

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

def maj_led(distance):
    global seuil
    print("MAJ LED")
    if (distance > seuil):
        pi.write(RED, 1)
        pi.write(GREEN, 0)
        pi.write(BLUE, 1)
    elif (distance <= seuil and distance > seuil/2):
        pi.write(RED, 0)
        pi.write(GREEN, 0)
        pi.write(BLUE, 1)
    else:
        pi.write(RED, 0)
        pi.write(GREEN, 1)
        pi.write(BLUE, 1)
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)