from flask import Flask, render_template, request, redirect, url_for
import random
import time

app = Flask(__name__)

# Variable pour stocker l'heure de début du stimulus
start_time = None

@app.route('/')
def index():
    """Page d'accueil avec un bouton pour commencer le test"""
    return render_template('index.html')

@app.route('/start')
def start():
    """Page pour attendre un délai aléatoire avant d'afficher le stimulus"""
    global start_time
    delay = random.uniform(2, 5)  # Délai aléatoire entre 2 et 5 secondes
    return render_template('stimulus.html', delay=delay)

@app.route('/react', methods=['POST'])
def react():
    """Page pour enregistrer la réaction"""
    global start_time
    start_time = request.form.get('start_time', type=float)  # Récupère l'heure de début
    reaction_time = (time.time() * 1000) - start_time  # Temps de réaction en millisecondes
    reaction_time_seconds = reaction_time / 1000  # Convertir en secondes
    return render_template('result.html', reaction_time=reaction_time_seconds)

if __name__ == '__main__':
    app.run(debug=True)
