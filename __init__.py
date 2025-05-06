from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
from collections import Counter

                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html') #commit
@app.route("/contact/")
def MaPremiereAPI():
    return "<h2>Ma page de contact</h2>"

@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def histogramme():
    return render_template("histogramme.html")

@app.route("/contact/")
def contact():
    return render_template("contact.html")


@app.route('/commits/')
def commits():
    # Récupérer les données de l'API GitHub
    response = urlopen('https://api.github.com/repos/gharbiines25/5MCSI_Metriques/commits')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))

    # Extraire les minutes des dates de commit
    minutes_list = []
    for commit in json_content:
        commit_date_str = commit.get('commit', {}).get('author', {}).get('date')
        if commit_date_str:
            date_object = datetime.strptime(commit_date_str, '%Y-%m-%dT%H:%M:%SZ')
            minutes_list.append(date_object.minute)

    # Compter le nombre de commits par minute
    minute_counter = Counter(minutes_list)

    # Préparer les données pour le graphique
    results = []
    for minute in range(0, 60):
        results.append({
            'minute': f"{minute} min",
            'nb_commits': minute_counter.get(minute, 0)
        })

    return render_template("commits.html", results=results)
  
if __name__ == "__main__":
  app.run(debug=True)
