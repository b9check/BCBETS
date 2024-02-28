from flask import Flask, render_template
from get_current_team_metrics import get_current_metrics
from compare_odds import get_DK_bets_analysis


current_metrics, rounded_metrics = get_current_metrics()
DK_analysis = get_DK_bets_analysis()

rounded_metrics.to_csv('rounded_metrics.csv', index=False)
DK_analysis.to_csv('DK_analysis.csv', index=False)