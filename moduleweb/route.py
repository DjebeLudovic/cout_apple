from flask import Blueprint, render_template, request, send_file
from model.predict import predict_future_prices
import matplotlib.pyplot as plt
import io
import pandas as pd

# Créer un Blueprint
routes = Blueprint(
    'routes', 
    __name__,
    template_folder='templates',
    static_folder='static',      
    static_url_path='/moduleweb/static'   
)

@routes.route("/index")
def index():
    return render_template('index.html')

@routes.route("/charts-echarts")
def charts_echarts():
    return render_template("charts-echarts.html")

@routes.route("/pages-contact")
def pages_contact():
    return render_template("pages-contact.html")

@routes.route("/pages-error-404")
def pages_error_404():
    return render_template("pages-error-404.html")


@routes.route("/tables-data", methods=['GET', 'POST'])
def tables_data():
    prediction_result = None
    prediction_days = None
    
    if request.method == 'POST':
        prediction_days = request.form.get('prediction_days', type=int)

        if prediction_days:
            input_date = pd.to_datetime(prediction_days, errors='coerce')

            # Effectuer la prédiction
            prediction_result = predict_future_prices(prediction_days)

    return render_template("tables-data.html", prediction=prediction_result, prediction_days=prediction_days)

@routes.route("/prediction-plot")
def prediction_plot():
    # Générer un graphique avec les prédictions
    predicted_prices = predict_future_prices(10)  # 10 jours
    
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, 11), predicted_prices, marker='o', label="Predicted Prices")
    plt.title("Predicted Future Prices for the Next 10 Days")
    plt.xlabel("Days")
    plt.ylabel("Predicted Price")
    plt.grid()
    plt.legend()
    
    # Sauvegarder l'image dans un buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    
    return send_file(buf, mimetype='image/png')