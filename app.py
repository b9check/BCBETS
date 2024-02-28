from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

@app.route('/')

def home():
    rounded_metrics = pd.read_csv('rounded_metrics.csv')
    DK_analysis = pd.read_csv('DK_analysis.csv')
    DK_html = DK_analysis.to_html(classes='table table-striped', index=False)
    metrics_html = rounded_metrics.to_html(classes='table table-striped', index=False)
    return render_template('index.html', table1_html=DK_html, table2_html=metrics_html)

if __name__ == '__main__':
    app.run(debug=True, port=8000)