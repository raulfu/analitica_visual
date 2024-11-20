from utils.helpers import df_players, create_plot
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# Group data for totals and averages
df_players_total = df_players.groupby('player')[['points', 'three_points_made', 'total_rebounds', 'assists', 'steals', 'blocks_favour', 'plus_minus']].sum()

#excluding 2024
df_players_until_2024 = df_players[df_players['season_code'] != 'E2024']

df_players_avg = df_players_until_2024.groupby('player')[['points_per_game', 'three_points_made_per_game', 'total_rebounds_per_game', 'assists_per_game', 'steals_per_game', 'blocks_favour_per_game', 'plus_minus_per_game']].mean()

# Create a mapping for the categories
categories = {
    "Points": ("points", "points_per_game"),
    "Three Pointers Made": ("three_points_made", "three_points_made_per_game"),
    "Rebounds": ("total_rebounds", "total_rebounds_per_game"),
    "Assists": ("assists", "assists_per_game"),
    "Steals": ("steals", "steals_per_game"),
    "Blocks": ("blocks_favour", "blocks_favour_per_game"),
    "Plus/Minus": ("plus_minus", "plus_minus_per_game"),
}

# Streamlit App
st.title("Top 10 Players in Various Categories")
st.sidebar.header("Select Category")

# Select category
selected_category = st.sidebar.selectbox("Choose a category", list(categories.keys()))

# Get column names for the selected category
total_col, per_game_col = categories[selected_category]

# Get top 10 data for totals and per-game statistics
top_10_totals = df_players_total[total_col].nlargest(10)
top_10_per_game = df_players_avg[per_game_col].nlargest(10)

# Layout with columns
col1, col2 = st.columns(2)

# Plot Total Chart
with col1:
    st.subheader(f"Top 10 Players by {selected_category} (Totals)")
    fig1 = create_plot(top_10_totals, f"Top 10 Players by {selected_category} (Totals)", "Player", "Total", color = 'plum')
    st.pyplot(fig1)

# Plot Per-Game Chart
with col2:
    st.subheader(f"Top 10 Players by {selected_category} (Per Game)")
    fig2 = create_plot(top_10_per_game, f"Top 10 Players by {selected_category} (Per Game)", "Player", "Per Game", color = 'mediumpurple')
    st.pyplot(fig2)


st.write("Excluding current season on per game stats because the small sample size. This small sample size is the few games that have already occurred in the current season. This entails that some players are playing their first season and the per_game statistics cannot be compared to whole history")














st.title("STREAMLIT BAR CHARTS")


# Streamlit App
st.title("Top 10 Players in Various Categories")
#st.sidebar.header("Select Category")

# Select category
#selected_category = st.sidebar.selectbox("Choose a category", list(categories.keys()))

# Get column names for the selected category
total_col, per_game_col = categories[selected_category]


# Get top 10 data for totals and per-game statistics
top_10_totals = df_players_total[total_col].nlargest(10)
top_10_per_game = df_players_avg[per_game_col].nlargest(10)

# Layout with columns
col1, col2 = st.columns(2)

# Plot Total Chart
with col1:
    st.subheader(f"Top 10 Players by {selected_category} (History Totals)")
    st.bar_chart(top_10_totals)

# Plot Per-Game Chart
with col2:
    st.subheader(f"Top 10 Players by {selected_category} Per Game")
    st.bar_chart(top_10_per_game)




