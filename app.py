from flask import Flask, render_template
from get_current_team_metrics import get_current_metrics
from compare_odds import get_DK_bets_analysis

app = Flask(__name__)

@app.route('/')

def home():
    current_metrics, rounded_metrics = get_current_metrics()
    metrics_html = rounded_metrics.to_html(classes='table table-striped', index=False)
    DK_analysis = get_DK_bets_analysis()
    print(DK_analysis)
    DK_html = DK_analysis.to_html(classes='table table-striped', index=False)
    return render_template('index.html', table1_html=DK_html, table2_html=metrics_html)

if __name__ == '__main__':
    app.run(debug=True)