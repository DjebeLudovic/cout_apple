from flask import Flask, render_template
from moduleweb.route import routes  # Importer les routes du Blueprint
import pandas as pd
import plotly.express as px
import plotly.io as pio
import os

app = Flask(__name__, template_folder="moduleweb/templates")
app.register_blueprint(routes)  # Enregistrer les routes du Blueprint

# Charger les données CSV
dataset_path = os.path.join(os.getcwd(), 'moduleweb', 'dataset', 'cours_apple_5.csv')
try:
    # Utilisez pandas pour charger un fichier CSV
    df = pd.read_csv(dataset_path)
except FileNotFoundError:
    df = pd.DataFrame()  # Créer un DataFrame vide si le fichier n'est pas trouvé
    print(f"Erreur : Le fichier CSV est introuvable ({dataset_path}).")
except pd.errors.EmptyDataError:
    df = pd.DataFrame()
    print("Erreur : Le fichier CSV est vide.")
except Exception as e:
    df = pd.DataFrame()
    print(f"Erreur : {e}")
print(f"Chemin du fichier CSV : {dataset_path}")

@app.route("/")
def index():
    # Vérifier que les données sont valides
    if df.empty:
        return render_template("index.html", chart_html=None)

    # Nettoyer les données (supprimer les valeurs vides et convertir les types)
    df["Date"] = pd.to_datetime(df["Date"], errors='coerce')  # Convertir les dates
    df["Clôture Ajustée"] = pd.to_numeric(df["Clôture Ajustée"].str.replace(',', '.'), errors='coerce')

    # Créer un graphique interactif avec Plotly
    fig = px.line(df, x='Date', y='Clôture Ajustée', title="Évolution boursière d'Apple",
                  labels={"Clôture Ajustée": "Prix de Clôture Ajustée", "Date": "Date"})
    
    # Convertir le graphique Plotly en HTML pour l'affichage
    chart_html = pio.to_html(fig, full_html=False)

    return render_template("index.html", chart_html=chart_html)

if __name__ == "__main__":
    app.run(debug=True)
