import streamlit as st
import pickle
import pandas as pd
from utils.helpers import simulate_season, df_teams, team_id_to_name

with open('../linear_regressor_points.pkl', 'rb') as f:
    linear_regressor = pickle.load(f)


st.title("Euroleague Team Record Predictor / Season Simulator")
st.write("""This app predicts the record of a Euroleague basketball team of the current season.
You can choose a team to get the prediction and the current season will be simulated using the model on linear regression.""")


# selection teams
teams_current_season = df_teams[df_teams['season_code'] == 'E2024']
team_to_simulate = st.selectbox("Choose team to simulate its season record", teams_current_season['team_name'].unique(), index=1)
team_id_to_simulate = df_teams.loc[df_teams['team_name'] == team_to_simulate, 'team_id'].iloc[0]


season_results = simulate_season(team_id_to_simulate, df_teams, linear_regressor)

# Print results
st.write(f"### Simulated Season Record for {team_to_simulate}: {season_results['wins']} Wins, {season_results['losses']} Losses")
st.write("Predicted Results of the 2024-2025 Season:\n")
st.write("\n")


# Layout with columns
col1, col2 = st.columns(2)

# Loop through each game result
i=1
for game in season_results['results']:
    # Map team IDs to names
    team_a_name = team_id_to_name.get(game['team_a'], "Unknown Team")
    team_b_name = team_id_to_name.get(game['team_b'], "Unknown Team")
    winner_name = team_id_to_name.get(game['winner'], "Unknown Team")

    # lo hago por pairs de partidos contra mismo equipo
    i+=1
    if i%2:
        with col1:
            st.write(f"{team_a_name} ({game['points_a']:.1f}) vs {team_b_name} ({game['points_b']:.1f}) - Winner: {winner_name}")
    else:
        with col2:
            st.write(f"{team_a_name} ({game['points_a']:.1f}) vs {team_b_name} ({game['points_b']:.1f}) - Winner: {winner_name}")
