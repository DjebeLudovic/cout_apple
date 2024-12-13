from flask import Blueprint, render_template

# Créer un Blueprint
routes = Blueprint('routes', __name__)

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

@routes.route("/tables-data")
def tables_data():
    return render_template("tables-data.html")
