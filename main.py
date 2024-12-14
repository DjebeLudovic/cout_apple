from flask import Flask, render_template, request
from moduleweb.route import routes  # Importer les routes du Blueprint
import pandas as pd
import plotly.express as px
import plotly.io as pio
import os

app = Flask(__name__, template_folder="moduleweb/templates")
app.register_blueprint(routes)  # Enregistrer les routes du Blueprint

# Charger les données CSV
dataset_path = os.path.join('moduleweb', 'dataset', 'cours_apple_5.csv')
try:
    df = pd.read_csv(dataset_path)
    df["Date"] = pd.to_datetime(df["Date"], errors='coerce')
    df["Année"] = df["Date"].dt.year.astype("Int64")  # Convertir l'année en entier
    df["Mois"] = df["Date"].dt.month  # Ajouter la colonne Mois
    df["Clôture Ajustée"] = pd.to_numeric(df["Clôture Ajustée"].str.replace(',', '.'), errors='coerce')
    df["Plus Haut"] = pd.to_numeric(df["Plus Haut"].str.replace(',', '.'), errors='coerce')
    df["Plus Bas"] = pd.to_numeric(df["Plus Bas"].str.replace(',', '.'), errors='coerce')
    df["Ferme"] = pd.to_numeric(df["Ferme"].str.replace(',', '.'), errors='coerce')
except FileNotFoundError:
    df = pd.DataFrame()
    print(f"Erreur : Le fichier CSV est introuvable ({dataset_path}).")
except pd.errors.EmptyDataError:
    df = pd.DataFrame()
    print("Erreur : Le fichier CSV est vide.")
except Exception as e:
    df = pd.DataFrame()
    print(f"Erreur : {e}")

@app.route("/", methods=["GET", "POST"])
def index():
    selected_year = None
    filtered_df = df

    # Récupérer l'année sélectionnée si le formulaire est soumis
    if request.method == "POST":
        selected_year = request.form.get("year_filter", "")
        if selected_year:
            selected_year = int(selected_year)  # Convertir l'année en entier
            filtered_df = df[df["Année"] == selected_year]

    # Dernières ventes (5 dernières lignes)
    recent_sales = filtered_df.tail(5).to_dict(orient="records")

    # Assurer que les dates de "Recent Sales" sont bien formatées
    for sale in recent_sales:
        if isinstance(sale['Date'], pd.Timestamp):
            sale['Date'] = sale['Date'].strftime('%d-%m-%Y')
        else:
            sale['Date'] = 'N/A'  # Si la date est invalide, afficher 'N/A'

    # Créer le graphique détaillé
    fig = px.line(
        filtered_df,
        x='Date',
        y='Clôture Ajustée',
        title=f"Évolution boursière d'Apple - {selected_year or 'Toutes les années'}",
        labels={"Clôture Ajustée": "Prix de Clôture Ajustée", "Date": "Date"},
        markers=True  # Afficher les marqueurs pour chaque point
    )

    # Personnalisation du graphique
    fig.update_traces(
        line=dict(width=3, color='rgb(0, 153, 255)')  # Modifier la couleur de la ligne
    )

    # Ajouter un zoom interactif et améliorer la mise en page
    fig.update_layout(
        xaxis_rangeslider_visible=True,  # Permettre un zoom sur l'axe X
        hovermode="x unified",  # Affichage des données lorsque l'on survole la ligne
        title="Évolution boursière d'Apple",
        showlegend=True,  # Afficher la légende pour la courbe
        xaxis=dict(
            showgrid=True,  # Afficher les lignes de grille
            tickformat="%d-%m-%Y",  # Formater les ticks de l'axe des X
            tickangle=-45  # Incliner les ticks pour une meilleure lisibilité
        ),
        yaxis=dict(
            showgrid=True,  # Afficher les lignes de grille
            zeroline=False  # Ne pas afficher la ligne zéro
        )
    )

    # Convertir le graphique Plotly en HTML
    chart_html = pio.to_html(fig, full_html=False)

    # Années disponibles pour le filtre
    years = sorted(df["Année"].dropna().unique())

    return render_template("index.html", chart_html=chart_html, years=years, selected_year=selected_year, recent_sales=recent_sales)

if __name__ == "__main__":
    app.run(debug=True)
