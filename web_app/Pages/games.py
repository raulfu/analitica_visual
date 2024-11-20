from utils.helpers import df_header
import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt

# Streamlit application
st.title("Game Analysis")

# Selectboxes to choose teams and season
teams = df_header['team_a'].unique()
team_a = st.selectbox("Select Local Team", options=teams, index = 67)
team_b = st.selectbox("Select Away Team", options=teams, index = 90)
#st.write(df_header['team_a'].nunique())

# Filter dataframe to show only games between selected teams
filtered_df = df_header[((df_header['team_a'] == team_a) & (df_header['team_b'] == team_b))]

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

    # Display game details
    st.write(f"#### {team_a} {selected_game['score_a']} vs {team_b} {selected_game['score_b']} ({selected_game['phase']} GAME ON {season} SEASON ON {selected_game['date']})")

    # Extract cumulative scores for the selected game
    quarters = ['score_quarter_1', 'score_quarter_2', 'score_quarter_3', 'score_quarter_4']
    cumulative_team_a = [selected_game[f"{q}_a"] for q in quarters]
    cumulative_team_b = [selected_game[f"{q}_b"] for q in quarters]

    # Compute points scored per quarter
    points_team_a = [cumulative_team_a[0]] + [cumulative_team_a[i] - cumulative_team_a[i-1] for i in range(1, len(cumulative_team_a))]
    points_team_b = [cumulative_team_b[0]] + [cumulative_team_b[i] - cumulative_team_b[i-1] for i in range(1, len(cumulative_team_b))]

    # Define quarter labels
    labels = ['Q1', 'Q2', 'Q3', 'Q4']




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



    # Streamlit application for Altair Charts
    st.write("##### Streamlit Altair Visualizations")

    # Points scored per quarter - Prepare data for Streamlit bar chart
    points_data = pd.DataFrame({
        "Quarter": labels * 2,
        "Team": [team_a] * 4 + [team_b] * 4,
        "Points": points_team_a + points_team_b
    })

    # Altair chart for points scored per quarter
    points_chart = alt.Chart(points_data).mark_bar().encode(
        x=alt.X('Quarter:N', title='Quarter'),
        y=alt.Y('Points:Q', title='Points Scored'),
        color=alt.Color('Team:N', scale=alt.Scale(domain=[team_a, team_b], range=['red', 'blue'])),
        tooltip=['Team', 'Points']
    ).properties(
        title="Points Scored Per Quarter",
        width=600,
        height=400
    )

    # Cumulative scores per quarter - Prepare data for Streamlit bar chart
    cumulative_data = pd.DataFrame({
        "Quarter": labels * 2,
        "Team": [team_a] * 4 + [team_b] * 4,
        "Cumulative Points": cumulative_team_a + cumulative_team_b
    })

    # Altair chart for cumulative scores per quarter
    cumulative_chart = alt.Chart(cumulative_data).mark_bar().encode(
        x=alt.X('Quarter:N', title='Quarter'),
        y=alt.Y('Cumulative Points:Q', title='Cumulative Points'),
        color=alt.Color('Team:N', scale=alt.Scale(domain=[team_a, team_b], range=['red', 'blue'])),
        tooltip=['Team', 'Cumulative Points']
    ).properties(
        title="Cumulative Scores Per Quarter",
        width=600,
        height=400
    )

    # Display Altair charts in two columns
    col1, col2 = st.columns(2)
    with col1:
        st.altair_chart(points_chart)
    with col2:
        st.altair_chart(cumulative_chart)
