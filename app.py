from flask import Flask, render_template, request, redirect, url_for, session, send_file
import time
import pandas as pd

app = Flask(__name__)
app.secret_key = 'une_cle_secrete_tres_complexe'

@app.route('/')
def index():
    """Page d'accueil avec un bouton pour commencer le test"""
    session.clear()
    session['results'] = {
        "Condition 1": [],  
        "Condition 2": [],  
        "Condition 3": [],  
        "Condition 4": []   
    }
    session['current_trial'] = 0
    session['current_condition'] = 1
    return render_template('index.html')

@app.route('/start_experiment')
def start_experiment():
    return redirect(url_for('condition'))

@app.route('/condition')
def condition():
    condition_id = session['current_condition']
    trial = session['current_trial']
    if trial < 5:
        return render_template(f'condition_{condition_id}.html', trial=trial + 1)
    else:
        return redirect(url_for('view_results'))

@app.route('/react', methods=['POST'])
def react():
    start_time = request.form['start_time']
    reaction_time = (time.time() * 1000) - float(start_time)
    condition_key = f"Condition {session['current_condition']}"

    session['results'][condition_key].append(reaction_time / 1000)

    session['current_trial'] += 1
    if session['current_trial'] == 5:
        session['current_trial'] = 0
        session['current_condition'] += 1
        if session['current_condition'] > 4:
            return redirect(url_for('view_results'))

    return redirect(url_for('condition'))

@app.route('/results')
def view_results():
    """Affiche un tableau des résultats pour chaque condition"""
    return render_template('results.html', results=session['results'])

@app.route('/download-excel')
def download_excel():
    data = []
    for condition, times in session['results'].items():
        for i, time in enumerate(times, 1):
            data.append({"Condition": condition, "Trial / Essai": f"Essai {i}", "Reaction Time / Temps de Réaction (s)": time})

    df = pd.DataFrame(data)
    excel_path = 'results.xlsx'
    with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
        
    return send_file(excel_path, as_attachment=True, download_name='Results.xlsx')

'''if __name__ == '__main__':
    app.run(debug=True)'''
