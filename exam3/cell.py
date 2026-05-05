from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('cell.html') # Le fichier cell doit être dans le dossier templates qui se trouve à la racine avec app.py

if __name__ == '__main__':
    app.run(host='192.168.22.1', port=8080)