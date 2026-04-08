from flask import Flask, jsonify, request
import socket
from datetime import datetime
import pigpio
from flask_cors import CORS

BTN = 16
RED = 20
GREEN = 17
BLUE = 27

app = Flask(__name__)
CORS(app)
pi = pigpio.pi()
pi.set_mode(BTN,pigpio.INPUT)

pi.set_mode(RED,pigpio.OUTPUT)
pi.set_mode(GREEN,pigpio.OUTPUT)
pi.set_mode(BLUE,pigpio.OUTPUT)

pi.set_PWM_range(RED,255)
pi.set_PWM_range(GREEN,255)
pi.set_PWM_range(BLUE,255)

@app.route('/info',methods=['GET'])
def info_hote():
  d = {}
  date = datetime.now()
  d['hote'] = socket.gethostname()
  d['date'] = date.strftime("%Y-%m-%d, %H:%M:%S")
  
  return jsonify(d)

@app.route('/bouton',methods=['GET'])
def get_bouton():
  d = {}
  d['etat'] = pi.read(BTN)
  
  return jsonify(d)

@app.route('/led', methods=['POST'])
def set_led():
    if request.method == "POST":
      json = request.get_json()
      if "etat" in json:
        if json["etat"].lower() == "red":
            pi.write(RED,0)
        elif json["etat"].lower() == "green":
            pi.write(GREEN,0)
        elif json["etat"].lower() == "blue":
            pi.write(BLUE,0)
        elif json["etat"].lower() == "off":
            pi.write(RED,1)
            pi.write(GREEN,1)
            pi.write(BLUE,1)
        else:
            return jsonify({'Erreur': 'Mauvaise valeur'}),500
      else:
        return jsonify({'Erreur': 'Mauvais attribut'}),500
    else:
      return jsonify({'Erreur': 'Requetes POST seulement'}),500
    return jsonify({'Etat': json["etat"]}),200

@app.route('/color', methods=['POST'])
def set_color():
    if request.method == "POST":
      json = request.get_json()
      if "color" in json:
        rgb = json['color'].split(',')
        pi.set_PWM_dutycycle(RED, 255-int(rgb[0]))
        pi.set_PWM_dutycycle(GREEN, 255-int(rgb[1]))
        pi.set_PWM_dutycycle(BLUE, 255-int(rgb[2]))
        print('PRINT----',rgb[0],rgb[1],rgb[2])
      else:
        return jsonify({'Erreur': 'Mauvais attribut'}),500
    else:
      return jsonify({'Erreur': 'Requetes POST seulement'}),500
    return jsonify({'Etat': json["color"]}),200
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)