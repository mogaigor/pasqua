from flask import Flask, render_template, redirect, url_for
import pandas as pd
import random

app = Flask(__name__)

df = pd.read_csv('pokemon (1).csv')
dati_pokemon = df
totale_punti = 100
raccolta = []

probabilita_rarita = ['Comune'] * 70 + ['Non Comune'] * 20 + ['Rara'] * 9 + ['Ultra Rara'] * 1

def apri_pacchetto():
    pacchetto = []
    punti_guadagnati = 0
    i = 0
    while i < 5:
        rarita = random.choice(probabilita_rarita)
        carte_disponibili = dati_pokemon[dati_pokemon['Rarità'] == rarita]
        if len(carte_disponibili) > 0:
            carta = carte_disponibili.iloc[random.randint(0, len(carte_disponibili) - 1)]
            pacchetto.append(carta.to_dict())
            if rarita == 'Comune':
                punti_guadagnati += 1
            elif rarita == 'Non Comune':
                punti_guadagnati += 10
            elif rarita == 'Rara':
                punti_guadagnati += 30
            elif rarita == 'Ultra Rara':
                punti_guadagnati += 104
            i += 1
    return pacchetto, punti_guadagnati

def salva_raccolta_su_file():
    raccolta_df = pd.DataFrame(raccolta)
    raccolta_df.to_csv('collezione.csv', index=False)

def carica_raccolta_da_file():
    global raccolta
    try:
        raccolta = pd.read_csv('collezione.csv').to_dict(orient='records')
    except FileNotFoundError:
        raccolta = []

carica_raccolta_da_file()

@app.route('/')
def home():
    return render_template('index.html', totale_punti=totale_punti, raccolta=raccolta)

@app.route('/apri_pacchetto', methods=['POST'])
def apri_pacchetto_route():
    global totale_punti, raccolta
    if totale_punti >= 10:
        totale_punti -= 10
        pacchetto, punti_guadagnati = apri_pacchetto()
        raccolta.extend(pacchetto)
        salva_raccolta_su_file()
        totale_punti += punti_guadagnati
    return redirect(url_for('home'))

@app.route('/mostra_raccolta', methods=['GET'])
def mostra_raccolta_route():
    return render_template('collezione.html', raccolta=raccolta)

@app.route('/mostra_punti', methods=['GET'])
def mostra_punti_route():
    return render_template('punti.html', totale_punti=totale_punti)

if __name__ == '__main__':
    app.run(debug=True)