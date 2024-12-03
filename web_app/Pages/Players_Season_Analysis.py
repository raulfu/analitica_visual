import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import pandas as pd
from utils.helpers import df_players

# Streamlit Page Title
st.title("Season Analysis: Player Performance")

# Sidebar for Inputs
st.sidebar.header("Filter Options")


# Common Inputs: Season and Statistic
seasons = df_players['season_code'].unique()
selected_season = st.sidebar.selectbox("Select Season", sorted(seasons), index=len(seasons) - 1)

statistics = [
    'points', 'total_rebounds', 'assists', 'steals', 'turnovers', 'blocks_favour',
    'blocks_against', 'valuation', 'plus_minus'
]
selected_stat = st.sidebar.selectbox("Select Statistic", statistics, index=7)


st.write(f"## Player Analysis: {selected_stat.title()} vs. Minutes Played ({selected_season})")

# Filter Player Data by Selected Season
filtered_players = df_players[df_players['season_code'] == selected_season]

if filtered_players.empty:
    st.write(f"No data available for players in season {selected_season}.")
else:
    # Create Altair Scatter Plot
    scatter_plot = alt.Chart(filtered_players).mark_circle(size=60).encode(
        x=alt.X('minutes', title='Minutes Played'),
        y=alt.Y(selected_stat, title=selected_stat.title()),
        color=alt.Color('team_id', legend=alt.Legend(title="Team")),
        tooltip=['player', 'team_id', 'minutes', selected_stat]
    ).properties(
        width=800,
        height=500
    ).interactive()

    st.altair_chart(scatter_plot, use_container_width=True)
