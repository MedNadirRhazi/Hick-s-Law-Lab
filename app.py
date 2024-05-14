from flask import Flask, render_template, request, redirect, url_for, session
import random
import time

app = Flask(__name__)
app.secret_key = 'une_cle_secrete_tres_complexe'

# Variable pour stocker l'heure de début du stimulus
start_time = None

'''results = {
    "Condition 1": [],
    "Condition 2": [],
    "Condition 3": [],
    "Condition 4": []
}'''

@app.route('/')
def index():
    """Page d'accueil avec un bouton pour commencer le test"""
    session.clear()
    session['results'] = {
        "Condition 1": [[] for _ in range(5)],  
        "Condition 2": [[] for _ in range(5)],  
        "Condition 3": [[] for _ in range(5)],  
        "Condition 4": [[] for _ in range(5)]   
    }
    session['current_trial'] = 0
    session['current_condition'] = 1
    return render_template('index.html')


@app.route('/start_experiment')
def start_experiment():
    return redirect(url_for('condition'))

@app.route('/condition')
def condition():
    trial = session['current_trial']
    condition_id = session['current_condition']
    if trial >= 5:
        return redirect(url_for('view_results'))  
    return render_template(f'condition_{condition_id}.html', trial=trial+1)

@app.route('/react', methods=['POST'])
def react():
    start_time = request.form['start_time']
    reaction_time = (time.time() * 1000) - float(start_time)
    condition_key = f"Condition {session['current_condition']}"

    
    session['results'][condition_key][session['current_trial']].append(reaction_time / 1000)

    
    next_condition = session['current_condition'] + 1
    if next_condition > 4:
        session['current_condition'] = 1
        session['current_trial'] += 1
    else:
        session['current_condition'] = next_condition

    return redirect(url_for('condition'))

@app.route('/results')
def view_results():
    """Affiche un tableau des résultats pour chaque condition"""
    return render_template('results.html', results=session['results'])



if __name__ == '__main__':
    app.run(debug=True)
