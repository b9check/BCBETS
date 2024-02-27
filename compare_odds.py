from draftkings_script import get_DK_moneylines
from get_current_team_metrics import get_current_metrics
from joblib import load
import pandas as pd


# For converting DraftKings team abbreviations to NBA API abbreviations
DK_to_API = {'MIL': 'MIL', 'PHI': 'PHI', 'LA L': 'LAL', 'PHO': 'PHX', 'DAL': 'DAL', 'IND': 'IND',
             'CLE': 'CLE', 'WAS': 'WAS', 'DEN': 'DEN', 'GS ': 'GSW', 'OKC': 'OKC', 'HOU': 'HOU',
             'CHI': 'CHI', 'NO ': 'NOP', 'ORL': 'ORL', 'ATL': 'ATL', 'SA ': 'SAS', 'UTA': 'UTA',
             'CHA': 'CHA', 'POR': 'POR', 'SAC': 'SAC', 'LA C': 'LAC', 'MIA': 'MIA', 'MEM': 'MEM',
             'TOR': 'TOR', 'DET': 'DET', 'NY ': 'NYK', 'BKN': 'BKN', 'MIN': 'MIN', 'BOS': 'BOS'}


# Converts a winning percentage (from model) to a fair line
def WP_to_line(win_percentage):
    Ratio = 1/win_percentage - 1
    Fair_Line = 0
    if Ratio <= 1:
        Fair_Line = "-"+str(int(100/Ratio))
    else:
        Fair_Line = "+"+str(int(100*Ratio))
    return Fair_Line


# Get difference between two lines
def get_line_diffs(current_lines, fair_lines):
    diffs = []
    for current_line, fair_line in zip(current_lines, fair_lines):
        current_line = int(current_line)
        fair_line = int(fair_line)
        if (current_line > 0 and fair_line > 0) or (current_line < 0 and fair_line < 0):
            diff = current_line-fair_line
        elif current_line > 0 and fair_line < 0:
            diff = (current_line-100)+abs(fair_line+100)
        else:
            diff = -(abs(current_line+100)+(fair_line-100))
        diffs.append(diff)
    return diffs

    
# Gets fair lines (from model) and DK lines
def get_DK_bets_analysis():
    # Load DK lines and current metrics
    bets = get_DK_moneylines()
    [current_metrics, rounded_metrics] = get_current_metrics()
    model = load('trained_model.joblib')
    scaler = load('scaler.joblib')
    fair_lines1 = []
    fair_lines2 = []

    for index, bet in bets.iterrows():
        team1 = DK_to_API[bet['Team 1']]
        team2 = DK_to_API[bet['Team 2']]
        team1_data = current_metrics[current_metrics['Team'] == team1]
        team2_data = current_metrics[current_metrics['Team'] == team2]
        elo1 = team1_data['ELO'].values[0]  # Assuming there's only one row for the team
        pm1 = team1_data['Last 10 Game Plus-Minus'].values[0]
        elo2 = team2_data['ELO'].values[0]  # Assuming there's only one row for the team
        pm2 = team2_data['Last 10 Game Plus-Minus'].values[0]
        x_data1 = pd.DataFrame({
            'ELO_DIFFERENCE': [elo1-elo2],
            'TEN_GAME_PM_DIFFERENCE': [pm1-pm2], 
            'HOME_AWAY': [0]
        })
        y_pred1 = model.predict(scaler.transform(x_data1))[0]
        fair_line1 = WP_to_line(y_pred1)
        fair_lines1.append(fair_line1)

        x_data2 = pd.DataFrame({
            'ELO_DIFFERENCE': [elo2-elo1],
            'TEN_GAME_PM_DIFFERENCE': [pm2-pm1], 
            'HOME_AWAY': [1]
        })
        y_pred2 = model.predict(scaler.transform(x_data2))[0]
        fair_line2 = WP_to_line(y_pred2)
        fair_lines2.append(fair_line2)

    diffs1 = get_line_diffs(bets['Team 1 Odds'], fair_lines1)
    diffs2 = get_line_diffs(bets['Team 2 Odds'], fair_lines2)
    better_bets = ['1' if diff1 >= diff2 else '2' for diff1, diff2 in zip(diffs1, diffs2)]
    
    winning_bets = []
    winning_bet_diffs = []
    abs_diff = []
    for index, bet in enumerate(better_bets):
        team = bets['Team '+bet].iloc[index]
        odds = bets['Team '+bet+' Odds'].iloc[index]
        winning_bet = team + ' ' + odds
        winning_bets.append(winning_bet)
        win_diff = diffs1[index] if bet == '1' else diffs2[index]
        if bet == '1':
            fair_line = int(fair_lines1[index])
        else:
            fair_line = int(fair_lines2[index])
        win_diff_percent = abs(round(win_diff/int(fair_line),2))
        winning_bet_diffs.append(win_diff_percent)
        abs_diff.append(win_diff)

    Summary = pd.DataFrame({
        'Matchup': bets['Team 1'] + ' @ ' + bets['Team 2'],
        #'Team 2': bets['Team 2'],
        'Line 1': bets['Team 1'] + ' ' + bets['Team 1 Odds'],
        # 'Fair Line 1': fair_lines1,
        #'Line 1 Difference': diffs1,
        'Line 2': bets['Team 2'] + ' ' + bets['Team 2 Odds'],
        # 'Fair Line 2': fair_lines2,
        #'Line 2 Difference': diffs2,
        'Best Bet': winning_bets,
        'Discount of Best Bet': winning_bet_diffs,
        #'Abs Diff': abs_diff
    })

    return Summary


if __name__ == "__main__":
    Summary = get_DK_bets_analysis()
    #print(Summary)


