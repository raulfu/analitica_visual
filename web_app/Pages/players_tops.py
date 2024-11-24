from utils.helpers import df_players, create_plot
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


df = df_players

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
selected_top = st.sidebar.selectbox("Choose a top number to display", [5, 10, 15, 20], index=1)

# Select category
selected_category = st.sidebar.selectbox("Choose a category", list(categories.keys()))

# Select season or all history
possible_years = list(df_players['season_code'].unique())
possible_years.append('Historical (2007-2024)')
selected_year = st.sidebar.selectbox("Choose a season or select historical stats", possible_years, index=18)

st.title(f"Top {selected_top} Players in {selected_category} in {selected_year}")

if selected_year != 'Historical (2007-2024)':
    df = df[df['season_code'] == selected_year]

df_total = df.groupby('player')[['points', 'three_points_made', 'total_rebounds', 'assists', 'steals', 'blocks_favour', 'valuation']].sum()

#excluding 2024
if selected_year == 'Historical (2007-2024)':
    df = df[df['season_code'] != 'E2024']
df_avg = df.groupby('player')[['points_per_game', 'three_points_made_per_game', 'total_rebounds_per_game', 'assists_per_game', 'steals_per_game', 'blocks_favour_per_game', 'valuation_per_game']].mean()




# Get column names for the selected category
total_col, per_game_col = categories[selected_category]

# Get top 10 data for totals and per-game statistics
top_10_totals = df_total[total_col].nlargest(selected_top)
top_10_per_game = df_avg[per_game_col].nlargest(selected_top)

# Layout with columns
col1, col2 = st.columns(2)

# Plot Total Chart
with col1:
    st.subheader(f"Top 10 Players by {selected_category} (Totals)")
    fig1 = create_plot(top_10_totals, f"Top 10 Teams by {selected_category} (Totals)", "Player", "Total", color = 'plum')
    st.pyplot(fig1)
    

# Plot Per-Game Chart
with col2:
    st.subheader(f"Top 10 Players by {selected_category} (Per Game)")
    fig2 = create_plot(top_10_per_game, f"Top 10 Teams by {selected_category} (Per Game)", "Player", "Per Game", color = 'mediumpurple')
    st.pyplot(fig2)


st.write("Excluding current season on per game stats because the small sample size. This small sample size is the few games that have already occurred in the current season. This entails that some players are playing their first season and the per_game statistics cannot be compared to whole history")














st.title("STREAMLIT BAR CHARTS")


# Streamlit App
st.title("Top 10 Players in Various Categories")

# Layout with columns
col1, col2 = st.columns(2)

# Plot Total Chart
with col1:
    st.subheader(f"Top 10 Players by {selected_category} (History Totals)")
    st.bar_chart(top_10_totals)
    st.write(top_10_totals)

# Plot Per-Game Chart
with col2:
    st.subheader(f"Top 10 Players by {selected_category} Per Game")
    st.bar_chart(top_10_per_game)
    st.write(top_10_per_game)




