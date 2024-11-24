import streamlit as st
import pickle
import pandas as pd
from utils.helpers import df_teams

st.set_page_config(layout="wide")

# Load the models
with open('../logistic_model.pkl', 'rb') as f:
    logistic_model = pickle.load(f)

with open('../rf_model.pkl', 'rb') as f:
    rf_model = pickle.load(f)

with open('../regressor_model.pkl', 'rb') as f:
    rf_regressor = pickle.load(f)


# Title and Description
st.title("Euroleague Game Outcome Predictor With Current Season Teams")
st.write("""
This app predicts the outcome of a basketball game between two teams based on their per-game stats.
You can choose two teams and provide their statistics to get predictions from Logistic Regression and Random Forest models.
""")


# selection teams
teams_current_season = df_teams[df_teams['season_code'] == 'E2024']

team_a_id = st.selectbox("Choose local team", teams_current_season['team_name'].unique(), index=1)
team_b_id = st.selectbox("Choose away team", teams_current_season['team_name'].unique())

# Fetch stats for both teams for the season E2024
team_a_stats = df_teams[(df_teams['team_name'] == team_a_id) & (df_teams['season_code'] == 'E2024')].iloc[0]
team_b_stats = df_teams[(df_teams['team_name'] == team_b_id) & (df_teams['season_code'] == 'E2024')].iloc[0]

# Define input features for the matchup
input_features = {
    'defensive_rebounds_a': team_a_stats['defensive_rebounds_per_game'],
    'offensive_rebounds_a': team_a_stats['offensive_rebounds_per_game'],
    'assists_a': team_a_stats['assists_per_game'],
    'three_points_made_a': team_a_stats['three_points_made_per_game'],
    'turnovers_a': team_a_stats['turnovers_per_game'],
    'blocks_favour_a': team_a_stats['blocks_favour_per_game'],
    'steals_a': team_a_stats['steals_per_game'],
    #'points_received_a': team_b_stats['points_received_per_game'],
    'defensive_rebounds_b': team_b_stats['defensive_rebounds_per_game'],
    'offensive_rebounds_b': team_b_stats['offensive_rebounds_per_game'],
    'assists_b': team_b_stats['assists_per_game'],
    'three_points_made_b': team_b_stats['three_points_made_per_game'],
    'turnovers_b': team_b_stats['turnovers_per_game'],
    'blocks_favour_b': team_b_stats['blocks_favour_per_game'],
    'steals_b': team_b_stats['steals_per_game'],
    #'points_received_b': team_a_stats['points_received_per_game'],
}


# Convert to DataFrame
input_data = pd.DataFrame([input_features])

# Predict
logistic_prediction = logistic_model.predict(input_data)[0]
rf_prediction = rf_model.predict(input_data)[0]

predicted_points = rf_regressor.predict(input_data)
predicted_points_a = predicted_points[0][0]
predicted_points_b = predicted_points[0][1]


# Prediction Button
if st.button("Predict Outcome"):
    # Convert to DataFrame
    input_data = pd.DataFrame([input_features])

    # Predict using both models
    logistic_prediction = logistic_model.predict(input_data)[0]
    rf_prediction = rf_model.predict(input_data)[0]

    # Display Predictions
    st.subheader("Predictions")
    st.write(f"Logistic Model Prediction: **{'Local Team Wins' if logistic_prediction == 1 else 'Away Team Wins'}**")
    st.write(f"Random Forest Prediction: **{'Local Team Wins' if rf_prediction == 1 else 'Away Team Wins'}**")

    if predicted_points_a > predicted_points_b:
        winner = "Local Team Wins"
    elif predicted_points_a < predicted_points_b:
        winner = "Away Team Wins"
    # Output predictions
    st.write(f"Prediction MultiOutput Regressor for Points: {winner}")
    st.write(f"Predicted Points Regressor - Local Team: {predicted_points_a:.2f}")
    st.write(f"Predicted Points Regressor - Away Team: {predicted_points_b:.2f}")
    

