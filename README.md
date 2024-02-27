# BCBETS

# File overview:

# get_current_team_metrics is dedicated to pulling nba_api stats 
# and using them to get each team's current ELO and past 10 game Plus-Minus.
# These are then used to predict upcoming game outcomes.

# draftkings_class creates a class "DraftKings" which is pulls a bunch of
# NBA betting data from DraftKings' website

# draftkings_script parses through the raw DraftKings website data to specifically 
# pull moneyline bets and organize them

# compare_odds predicts win percentages for each game on DK's moneyline bets, then
# converts that into a "fair line", compares this fair line with the actual line,
# and calculates the percentage difference. This information is then displayed on the
# website and used to assess which bets are good.

# trained_model.jpblib is the trained model, and scaler.joblib is the scaler which is used
# to scale data before it is fed into the model for predictions.
