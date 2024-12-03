import streamlit as st
import pickle
import pandas as pd
from utils.helpers import df_teams
from utils.helpers_models import linear_regressor, logistic_model, svr_regressor, rf_model, gb_regressor



st.title("Euroleague Game Outcome Predictor With Current Season Teams")
st.write("""This app predicts the outcome of a Euroleague basketball game between two teams based on their per-game stats of the current season.
You can choose two teams to get predictions either from a simple perspective of who would win or from the perspective of how many points will each team score.""")
st.write("Therefore, we provide different models in an interactive way")


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
    'defensive_rebounds_b': team_b_stats['defensive_rebounds_per_game'],
    'offensive_rebounds_b': team_b_stats['offensive_rebounds_per_game'],
    'assists_b': team_b_stats['assists_per_game'],
    'three_points_made_b': team_b_stats['three_points_made_per_game'],
    'turnovers_b': team_b_stats['turnovers_per_game'],
    'blocks_favour_b': team_b_stats['blocks_favour_per_game'],
    'steals_b': team_b_stats['steals_per_game'],
}


# Convert to DataFrame
input_data = pd.DataFrame([input_features])


#select model
type_of_output = st.selectbox("Select the type of output", ["Simple (Who Wins?)", "Multi (How Many Points Will Each Team Score?)"], index=1)


if type_of_output == "Simple (Who Wins?)": # Predict simple solo quien gana

    model_selected = st.selectbox("Choose simple model", ["Logistic", "Random Forest"])

    if model_selected == "Logistic":
        simple_prediction = logistic_model.predict(input_data)[0]
    else:
        simple_prediction = rf_model.predict(input_data)[0]
        
else:
    model_selected = st.selectbox("Choose a multioutput model", ["Linear Regression", "Gradient Boosting", "Support Vector Regressor"])

    if model_selected == "Linear Regression":
        predicted_points = linear_regressor.predict(input_data)
    elif model_selected == "Gradient Boosting":
        predicted_points = gb_regressor.predict(input_data)
    else:
        predicted_points = svr_regressor.predict(input_data)
    
    predicted_points_a = predicted_points[0][0]
    predicted_points_b = predicted_points[0][1]




# Prediction Button
if st.button("Predict Outcome"):

    # Display Predictions

    if type_of_output == "Simple (Who Wins?)":
        st.write("### Simple Output On Who Wins")
        st.write(f"## {model_selected} Prediction: **{'Local Team Wins' if simple_prediction == 1 else 'Away Team Wins'}**")

    else:
        st.write("### Multi Output On How How Many Points Will Each Team Score")
        if predicted_points_a > predicted_points_b:
            winner = "Local Team Wins"
        elif predicted_points_a < predicted_points_b:
            winner = "Away Team Wins"
        # Output predictions
        st.write(f"## Prediction {model_selected} for Points: {winner}")
        st.write(f"### Predicted Points - Local Team: {predicted_points_a:.2f}")
        st.write(f"### Predicted Points - Away Team: {predicted_points_b:.2f}")


    

