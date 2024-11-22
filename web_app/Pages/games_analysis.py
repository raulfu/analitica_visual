from utils.helpers import df_header, df_box_score
import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt

# Streamlit application
st.title("Game Analysis")

# Selectboxes to choose teams and season
teams = df_header['team_id_a'].unique()
team_id_a = st.selectbox("Select Local Team", options=teams, index = 18)
team_id_b = st.selectbox("Select Away Team", options=teams, index = 20)
#st.write(df_header['team_id_a'].nunique())

# Filter dataframe to show only games between selected teams
filtered_df = df_header[((df_header['team_id_a'] == team_id_a) & (df_header['team_id_b'] == team_id_b))]

# Get unique seasons for the selected teams
seasons = filtered_df['season_code'].unique()
season = st.selectbox("Select Season", options=seasons)

# Filter the dataframe by selected season
if season is None:
    st.write('## No games for those teams')

else:
    season_df = filtered_df[filtered_df['season_code'] == season]

    # Select the game from the filtered data
    games = season_df['game_id'].unique()  # Assuming 'game_id' is a unique identifier for games
    game_id = st.selectbox("Select Game", options=games)


    # Extract the selected game's data
    selected_game = season_df[season_df['game_id'] == game_id].iloc[0]
    team_a = selected_game['team_a']
    team_b = selected_game['team_b']

    # Display game details
    st.write(f"#### {team_a} {selected_game['score_a']} vs {selected_game['score_b']} {team_b} ({selected_game['phase']} GAME ON {season} SEASON ON {selected_game['date']})")


    # Extract cumulative scores for the selected game
    quarters = ['score_quarter_1', 'score_quarter_2', 'score_quarter_3', 'score_quarter_4']
    cumulative_team_a = [selected_game[f"{q}_a"] for q in quarters]
    cumulative_team_b = [selected_game[f"{q}_b"] for q in quarters]

    # Check for extra time and include them if they exist
    extra_time_labels = []
    extra_time_scores_team_a = []
    extra_time_scores_team_b = []

    for i in range(1, 5):  # Extra time quarters 1 through 4
        extra_time_label = f"score_extra_time_{i}"
        if not pd.isna(selected_game[f"{extra_time_label}_a"]):  # Check if the extra time score exists
            extra_time_labels.append(f"EQ{i}")
            extra_time_scores_team_a.append(selected_game[f"{extra_time_label}_a"])
            extra_time_scores_team_b.append(selected_game[f"{extra_time_label}_b"])

    # Add the extra time scores to the cumulative scores
    cumulative_team_a += extra_time_scores_team_a
    cumulative_team_b += extra_time_scores_team_b

    # Compute points scored per quarter, including extra time
    points_team_a = [cumulative_team_a[0]] + [cumulative_team_a[i] - cumulative_team_a[i - 1] for i in range(1, len(cumulative_team_a))]
    points_team_b = [cumulative_team_b[0]] + [cumulative_team_b[i] - cumulative_team_b[i - 1] for i in range(1, len(cumulative_team_b))]

    # Define labels, including extra time labels
    labels = ['Q1', 'Q2', 'Q3', 'Q4'] + extra_time_labels

    
    
    # Matplotlib visualizations
    st.write("##### Matplotlib Visualizations")

    # Set up the figure and axes
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Set the background color of the entire figure
    fig.patch.set_facecolor('black')

    # Set the background color of each subplot
    for ax in axes:
        ax.set_facecolor('black')  # Set the background of each subplot to black
        ax.tick_params(axis='both', colors='white')  # Set the tick color to white
        ax.set_xlabel(ax.get_xlabel(), color='white')  # Set xlabel text color to white
        ax.set_ylabel(ax.get_ylabel(), color='white')  # Set ylabel text color to white
        ax.set_title(ax.get_title(), color='white')  # Set title text color to white

    # Subplot 1: Points scored per quarter
    x = range(len(labels))
    width = 0.4
    axes[0].bar([p - width/2 for p in x], points_team_a, width=width, label=team_a, color='red')
    axes[0].bar([p + width/2 for p in x], points_team_b, width=width, label=team_b, color='blue')
    axes[0].set_xticks(x)
    axes[0].set_xticklabels(labels)
    axes[0].set_title('Points Scored Per Quarter', fontsize=16)
    axes[0].set_xlabel('Quarter', fontsize=14)
    axes[0].set_ylabel('Points', fontsize=14)
    axes[0].legend()
    axes[0].grid(axis='y', alpha=0.3)

    # Subplot 2: Cumulative scores per quarter
    axes[1].bar([p - width/2 for p in x], cumulative_team_a, width=width, label=team_a, color='red')
    axes[1].bar([p + width/2 for p in x], cumulative_team_b, width=width, label=team_b, color='blue')
    axes[1].set_xticks(x)
    axes[1].set_xticklabels(labels)
    axes[1].set_title('Cumulative Scores Per Quarter', fontsize=16)
    axes[1].set_xlabel('Quarter', fontsize=14)
    axes[1].set_ylabel('Cumulative Points', fontsize=14)
    axes[1].legend()
    axes[1].grid(axis='y', alpha=0.3)

    # Adjust layout
    plt.tight_layout()

    # Display the plot in Streamlit
    st.pyplot(fig)



    #box scores
    game_box_score = df_box_score[df_box_score['game_id'] == game_id]
    game_box_score = game_box_score.drop(columns = ['season_code', 'game_player_id', 'game_id', 'game', 'round', 'phase', 'player_id'])

    team_a_box_score = game_box_score[game_box_score['team_id'] == team_id_a]
    team_b_box_score = game_box_score[game_box_score['team_id'] == team_id_b]

    team_a_box_score_totals = team_a_box_score[team_a_box_score['dorsal'] == 'TOTAL'].drop(columns = ['is_starter', 'is_playing', 'plus_minus', 'dorsal'])
    team_b_box_score_totals = team_b_box_score[team_b_box_score['dorsal'] == 'TOTAL'].drop(columns = ['is_starter', 'is_playing', 'plus_minus', 'dorsal'])

    

    
    
    
    st.write(f"{team_a} BOX SCORE")
    st.write(team_a_box_score[team_a_box_score['dorsal'] != 'TOTAL'])


    st.write(f"{team_a} TOTALS")
    st.write(team_a_box_score_totals)


    st.write(f"{team_b} BOX SCORE")
    st.write(team_b_box_score[team_b_box_score['dorsal'] != 'TOTAL'])


    st.write(f"{team_b} TOTALS")
    st.write(team_b_box_score_totals)
        

