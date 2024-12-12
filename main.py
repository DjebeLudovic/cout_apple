from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

# Charger les données JSON
try:
    with open('../cout_apple/moduleweb/dataset/cleaned_cours_apple.json', 'r') as file:
        data = json.load(file)
except FileNotFoundError:
    data = []
    print("Erreur : Le fichier JSON est introuvable.")
except json.JSONDecodeError:
    data = []
    print("Erreur : Le fichier JSON est mal formaté.")

@app.route("/")
def index():
    if not data:
        return render_template("index.html", chart_dates=[], chart_closing_prices=[])

    # Extraire les colonnes nécessaires pour le graphique
    chart_dates = []
    chart_closing_prices = []
    try:
        chart_dates = [entry["Date"] for entry in data if "Date" in entry and entry["Date"]]
        chart_closing_prices = [float(entry["Clôture Ajustée"].replace(',', '.')) for entry in data if "Clôture Ajustée" in entry and entry["Clôture Ajustée"]]
    except KeyError as e:
        print(f"Erreur : Clé manquante dans le fichier JSON - {e}")
    except ValueError as e:
        print(f"Erreur lors de la conversion des valeurs : {e}")

    # Assurez-vous qu'il n'y a pas de valeur undefined
    chart_dates = [date for date in chart_dates if date is not None]
    chart_closing_prices = [price for price in chart_closing_prices if price is not None]
    if chart_dates is None:
    chart_dates = []
    return render_template("index.html", chart_dates=chart_dates, chart_closing_prices=chart_closing_prices)
if __name__ == "__main__":
    app.run(debug=True)
