import pigpio
from flask import Flask, jsonify, request
from flask_cors import CORS
import threading
import time

app = Flask(__name__)
CORS(app)

pi = pigpio.pi()

BTN = 26
R1 = 22
B1 = 17
G1 = 27

R2 = 6
B2 = 5
G2 = 16

rc1 = 255
gc1 = 255
bc1 = 255

rc2 = 255
gc2 = 255
bc2 = 255

NIVEAU_ROBUSTESSE = 3
isActive = False

pi.set_mode(BTN, pigpio.INPUT)

pi.set_mode(R1, pigpio.OUTPUT)
pi.set_mode(B1, pigpio.OUTPUT)
pi.set_mode(G1, pigpio.OUTPUT)

pi.set_mode(R2, pigpio.OUTPUT)
pi.set_mode(B2, pigpio.OUTPUT)
pi.set_mode(G2, pigpio.OUTPUT)

@app.route('/api/update_mood', methods=['POST'])
def update_mood():
    global isActive, rc1, gc1, bc1, rc2, gc2, bc2

    if request.method == "POST":
        json = request.get_json()
        if 'id' in json and isActive:
            id = json['id']
            if 'val' in json:
                try:
                    val = int(json['val'])
                    if id == 1:
                        rc1 = 255-val
                        gc1 = 255-val*0.5
                        bc1 = 255
                    elif id == 2:
                        rc2 = 255-val*0.2
                        gc2 = 255-val*0.8
                        bc2 = 255-val
                except:
                    print('La valeur doit être un nombre')
            else:
                return jsonify({'Erreur': 'Mauvaise attribut (val)'}),500
        else:
            return jsonify({'Erreur': 'Mauvaise attribut (id)'}),500
    else:
        return jsonify({'Erreur': 'Requetes POST seulement'}),500
    return jsonify({}),200

@app.route('/api/hardware_status', methods=['GET'])
def hardware_status():
    global isActive
    d = {'active':isActive}
    return jsonify(d)

def logique_interne():
    global isActive, rc1, gc1, bc1, rc2, gc2, bc2
    prev = 1
    while True:
        etat = pi.read(BTN)
        if etat != prev:
            somme = 0
            isNew = True
            for i in range(NIVEAU_ROBUSTESSE):
                if pi.read(BTN) != etat:
                    isNew = False
                    break
                time.sleep(0.01)
            if isNew: 
                prev = etat
                if etat == 0:
                    isActive = not isActive

        if isActive:
            pi.set_PWM_dutycycle(R1, rc1)
            pi.set_PWM_dutycycle(G1, gc1)
            pi.set_PWM_dutycycle(B1, bc1)

            pi.set_PWM_dutycycle(R2, rc2)
            pi.set_PWM_dutycycle(G2, gc2)
            pi.set_PWM_dutycycle(B2, bc2)
        else:
            pi.set_PWM_dutycycle(R1, 255)
            pi.set_PWM_dutycycle(G1, 255)
            pi.set_PWM_dutycycle(B1, 255)

            pi.set_PWM_dutycycle(R2, 255)
            pi.set_PWM_dutycycle(G2, 255)
            pi.set_PWM_dutycycle(B2, 255)

        time.sleep(0.02)

if __name__ == '__main__':
    try:
        thread_btn = threading.Thread(target=logique_interne, daemon=True)
        thread_btn.start()
        app.run(host='0.0.0.0',port=5000)
    except KeyboardInterrupt:
        thread_btn.join()