from flask import Flask, render_template, request, redirect, url_for
import random
import time

app = Flask(__name__)

# Variable pour stocker l'heure de début du stimulus
start_time = None

results = {
    "Condition 1": [],
    "Condition 2": [],
    "Condition 3": [],
    "Condition 4": []
}

@app.route('/')
def index():
    """Page d'accueil avec un bouton pour commencer le test"""
    return render_template('index.html')

@app.route('/condition/1')
def condition_1():
    """Page pour attendre un délai aléatoire avant d'afficher le stimulus"""
    global start_time
    delay = random.uniform(2, 5)  # Délai aléatoire entre 2 et 5 secondes
    return render_template('stimulus.html', delay=delay)

@app.route('/condition/2')
def condition_2():
    """Affiche la page pour la condition 2 avec 2 carrés"""
    return render_template('condition_2.html')

@app.route('/condition/3')
def condition_3():
    """Affiche la page pour la condition 3 avec 4 carrés"""
    return render_template('condition_3.html')

@app.route('/condition/4')
def condition_4():
    """Affiche la page pour la condition 4 avec 8 carrés"""
    return render_template('condition_4.html')

@app.route('/react/<int:condition_id>', methods=['POST'])
def react(condition_id):
    """Enregistre le temps de réaction pour une condition donnée"""
    start_time = request.form.get('start_time', type=float)
    reaction_time = (time.time() * 1000) - start_time
    reaction_time_seconds = reaction_time / 1000

    # Ajouter les résultats pour la condition spécifique
    results[f"Condition {condition_id}"].append(reaction_time_seconds)
    
    if condition_id == 1:
        return redirect(url_for('condition_2'))
    elif condition_id == 2:
        return redirect(url_for('condition_3'))
    elif condition_id == 3:
        return redirect(url_for('condition_4'))
    else:
        return redirect(url_for('view_results'))

@app.route('/results')
def view_results():
    """Affiche un tableau des résultats pour chaque condition"""
    return render_template('results.html', results=results)



if __name__ == '__main__':
    app.run(debug=True)
