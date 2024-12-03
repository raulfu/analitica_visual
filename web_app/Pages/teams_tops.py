from utils.helpers import df_teams
import pandas as pd
import streamlit as st
import altair as alt


df = df_teams

# Create a mapping for the categories
categories = {
    "Points": ("points", "points_per_game"),
    "Three Pointers Made": ("three_points_made", "three_points_made_per_game"),
    "Rebounds": ("total_rebounds", "total_rebounds_per_game"),
    "Assists": ("assists", "assists_per_game"),
    "Steals": ("steals", "steals_per_game"),
    "Blocks": ("blocks_favour", "blocks_favour_per_game"),
    "Valuation": ("valuation", "valuation_per_game"),
}

# Streamlit App
st.sidebar.header("TOPS")

# Select top
selected_top = st.sidebar.selectbox("Choose a top number to display", [5, 10, 15, 20, 30, 50], index=2)

# Select category
selected_category = st.sidebar.selectbox("Choose a category", list(categories.keys()))

# Select season or all history
possible_years = list(df_teams['season_code'].unique())
possible_years.append('Historical (2007-2024)')
selected_year = st.sidebar.selectbox("Choose a season or select historical stats", possible_years, index=18)

st.title(f"Top {selected_top} Teams in {selected_category} in {selected_year}")

if selected_year != 'Historical (2007-2024)':
    df = df[df['season_code'] == selected_year]



#excluding 2024
if selected_year == 'Historical (2007-2024)':
    df = df[df['season_code'] != 'E2024']


# Add games_played and seasons_played to the grouped data
df_total = df.groupby('team_name')[['points', 'three_points_made', 'total_rebounds', 'assists', 'steals', 'blocks_favour', 'valuation', 'games_played']].sum()
df_avg = df.groupby('team_name').agg(
    {
        'points_per_game': 'mean',
        'three_points_made_per_game': 'mean',
        'total_rebounds_per_game': 'mean',
        'assists_per_game': 'mean',
        'steals_per_game': 'mean',
        'blocks_favour_per_game': 'mean',
        'valuation_per_game': 'mean',
        'games_played': 'sum',  # Sum of games played
    }
)
df_seasons_played = df.groupby('team_name')['season_code'].nunique().reset_index().rename(columns={'season_code': 'seasons_played'})

# Merge seasons_played into df_total and df_avg
df_total = df_total.merge(df_seasons_played, on='team_name')
df_avg = df_avg.merge(df_seasons_played, on='team_name')

# Get column names for the selected category
total_col, per_game_col = categories[selected_category]

# Get top teams data for totals and per-game statistics
top_10_totals = df_total.nlargest(selected_top, total_col).reset_index()
top_10_per_game = df_avg.nlargest(selected_top, per_game_col).reset_index()

# Layout with columns
col1, col2 = st.columns(2)

# Plot Total Chart
with col1:
    st.subheader(f"Top {selected_top} Teams by {selected_category} ({selected_year})")
    chart = (
        alt.Chart(top_10_totals)
        .mark_bar()
        .encode(
            x=alt.X('team_name', sort='-y', title='Team'),
            y=alt.Y(total_col, title=selected_category),
            color=alt.Color('team_name', legend=None),
            tooltip=[
                alt.Tooltip('team_name', title='Team'),
                alt.Tooltip(total_col, title=selected_category),
                alt.Tooltip('games_played', title='Games Played'),
                alt.Tooltip('seasons_played', title='Seasons Played'),
            ],
        )
        .properties(width=400, height=400)
    )
    st.altair_chart(chart, use_container_width=True)

# Plot Per-Game Chart
with col2:
    st.subheader(f"Top {selected_top} Teams by {selected_category} Per Game ({selected_year})")
    chart_per_game = (
        alt.Chart(top_10_per_game)
        .mark_bar()
        .encode(
            x=alt.X('team_name', sort='-y', title='Team'),
            y=alt.Y(per_game_col, title=f"{selected_category} Per Game"),
            color=alt.Color('team_name', legend=None),
            tooltip=[
                alt.Tooltip('team_name', title='Team'),
                alt.Tooltip(per_game_col, title=f"{selected_category} Per Game"),
                alt.Tooltip('games_played', title='Games Played'),
                alt.Tooltip('seasons_played', title='Seasons Played'),
            ],
        )
        .properties(width=400, height=400)
    )
    st.altair_chart(chart_per_game, use_container_width=True)


st.write("A minimum of games played is not required because if a team exists in the dataset, it has already played a full season")

if selected_year == 'Historical (2007-2024)':
    st.write(
        "Excluding current season for per game stats on Historical because of the small sample (not many games have been played this season)"
    )






