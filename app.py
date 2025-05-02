from flask import Flask, render_template, redirect, url_for
import pandas as pd
import random

app = Flask(__name__)

df = pd.read_csv('pokemon (1).csv')
dati_pokemon = df
totale_punti = 100
raccolta = []

df_comune = dati_pokemon[dati_pokemon["Rarità"] == "Comune"]
df_non_comune = dati_pokemon[dati_pokemon["Rarità"] == "Non Comune"]
df_raro = dati_pokemon[dati_pokemon["Rarità"] == "Rara"]

def pesca():
    global totale_punti, raccolta
    pacchetto = []
    if totale_punti >= 10:
        totale_punti -= 10
        for _ in range(5):
            numero = random.randint(1, 100)
            if numero <= 70:
                totale_punti += 1
                pokemon = df_comune.sample().to_dict(orient='records')[0]
                pacchetto.append(pokemon)
            elif numero > 70 and numero <= 90:
                totale_punti += 3
                pokemon = df_non_comune.sample().to_dict(orient='records')[0]
                pacchetto.append(pokemon)
            elif numero > 90:
                totale_punti += 6
                pokemon = df_raro.sample().to_dict(orient='records')[0]
                pacchetto.append(pokemon)
        raccolta.extend(pacchetto)
        salva_raccolta_su_file()
    return pacchetto

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
    global totale_punti
    if totale_punti >= 10:
        pesca()
    return redirect(url_for('home'))

@app.route('/mostra_raccolta', methods=['GET'])
def mostra_raccolta_route():
    return render_template('index.html', raccolta=raccolta)

@app.route('/mostra_punti', methods=['GET'])
def mostra_punti_route():
    return render_template('index.html', totale_punti=totale_punti)

if __name__ == '__main__':
    app.run(debug=True)