import pigpio
from time import sleep
from flask_cors import CORS
from flask import Flask, jsonify, request
import threading


pi = pigpio.pi()
app = Flask(__name__)
CORS(app)

NIVEAU_ROBUSTESSE = 3
BTN = 26
pi.set_mode(BTN, pigpio.INPUT)

isOn = True

R = 17
G = 27
B = 22

redColor = 255
greenColor = 255
blueColor = 255

pi.set_mode(R, pigpio.OUTPUT)
pi.set_mode(G, pigpio.OUTPUT)
pi.set_mode(B, pigpio.OUTPUT)

pi.set_PWM_frequency(R, 800)
pi.set_PWM_frequency(G, 800)
pi.set_PWM_frequency(B, 800)
pi.set_PWM_range(R, 255)
pi.set_PWM_range(G, 255)
pi.set_PWM_range(B, 255)

@app.route('/api/set_rgb', methods=['POST'])
def set_rgb():
    global redColor, greenColor, blueColor
    print('IN ---- SET')
    if isOn:
        if request.method == 'POST':
            json = request.get_json()
            if 'R' in json and 'G' in json and 'B' in json:
                redColor = 255-int(json['R'])
                greenColor = 255-int(json['G'])
                blueColor = 255-int(json['B'])
            else: return jsonify({'Erreur': 'Mauvais attribut'}),500
        else: 
            return jsonify({'Erreur': 'Requetes POST seulement'}),500
    return jsonify({'Etat': 0})

@app.route('/api/led_state', methods=['GET'])
def led_state():
    global isOn
    d = {}
    d['power'] = isOn
    return jsonify(d)

def boutton():
    global isOn
    prev = pi.read(BTN)
    while True:
        while True:
            etat = pi.read(BTN)
            # print(etat)
            if etat != prev:
                somme = 0
                isNew = True
                for i in range(NIVEAU_ROBUSTESSE):
                    if pi.read(BTN) != etat:
                        isNew = False
                        break
                    sleep(0.01)
                if isNew: 
                    prev = etat
                    if etat == 0:
                        print("click")
                        isOn = not isOn
            sleep(0.02)

            if isOn:
                pi.set_PWM_dutycycle(R, redColor)
                pi.set_PWM_dutycycle(G, greenColor)
                pi.set_PWM_dutycycle(B, blueColor)
            else:
                pi.set_PWM_dutycycle(R, 255)
                pi.set_PWM_dutycycle(G, 255)
                pi.set_PWM_dutycycle(B, 255)

if __name__ == "__main__":
    thread_btn = threading.Thread(target=boutton, daemon=True)
    thread_btn.start()
    app.run(host='0.0.0.0', port=5000)