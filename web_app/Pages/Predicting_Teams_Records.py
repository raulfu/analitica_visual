import streamlit as st
from utils.helpers import simulate_season, df_teams, team_id_to_name
from utils.helpers_models import linear_regressor
import pandas as pd
import plotly.express as px


def Predicting_Teams_Records_main():

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
    st.write("See line chart of games below")
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


    # Prepare data for visualization
    results_df = pd.DataFrame(season_results['results'])
    results_df['team_a_name'] = results_df['team_a'].map(team_id_to_name)
    results_df['team_b_name'] = results_df['team_b'].map(team_id_to_name)

    st.write(f"### Points Scored Evolution (White Points Indicate {team_to_simulate})")
    st.write(f"The season was simulated doing 'ida y vuelta' between each team. Therefore, if index is even, the local team (team_a) is {team_to_simulate}. If index even, {team_to_simulate} is the away team (team_b)")
    


        # Add a column for white dot points
    results_df['white_dot_points'] = results_df.apply(
        lambda row: row['points_a'] if row.name % 2 == 0 else row['points_b'], axis=1
    )

    # Create a scatter trace for white dots
    scatter_white_dots = px.scatter(
        results_df,
        x=results_df.index,
        y='white_dot_points',
        labels={'white_dot_points': 'White Dot Points'},
        color_discrete_sequence=['white'],  # White color for dots
        title="Game-by-Game Points Evolution with Highlights"
    )

    # Create a line plot for points scored evolution
    fig = px.line(
        results_df,
        x=results_df.index,
        y=['points_a', 'points_b'],
        labels={'points_a': 'Points (Local Team)', 'points_b': 'Points (Opponent)'},
        title="Game-by-Game Points Evolution",
        markers=True
    )

    # Combine the line chart and scatter plot
    fig.add_trace(scatter_white_dots.data[0])  # Add the white dots trace to the line chart

    # Update layout for visibility
    fig.update_traces(marker=dict(size=10, line=dict(width=2, color='black')),  # Add black border to white dots
                    selector=dict(mode='markers'))

    # Show the updated plot
    st.plotly_chart(fig)
