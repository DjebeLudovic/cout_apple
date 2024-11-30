from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def init():
    return render_template('index.html')

@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/charts-echarts")
def charts_echarts():
    return render_template("charts-echarts.html")

@app.route("/pages-contact")
def pages_contact():
    return render_template("pages-contact.html")

@app.route("/pages-error-404")
def pages_error_404():
    return render_template("pages-error-404.html")

@app.route("/tables-data")
def tables_data():
    return render_template("tables-data.html")

if __name__ == "__main__":
    app.run(debug=True)

