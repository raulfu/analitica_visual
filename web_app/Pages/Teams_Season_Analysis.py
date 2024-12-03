import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
import pandas as pd
from utils.helpers import df_teams, df_box_score, df_players

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
selected_stat = st.sidebar.selectbox("Select Statistic", statistics)


st.write(f"## Team Analysis: {selected_stat.title()} Across Rounds ({selected_season})")

# Filter Box Score Data by Selected Season and 'dorsal' == 'TOTAL'
filtered_box_score = df_box_score[
    (df_box_score['season_code'] == selected_season) & (df_box_score['dorsal'] == 'TOTAL')
]

if filtered_box_score.empty:
    st.write(f"No data available for teams in season {selected_season}.")
else:
    # Group by Round and Team, then Aggregate the Selected Statistic
    team_stats_by_round = (
        filtered_box_score
        .groupby(['round', 'team_id'])[selected_stat]
        .sum()
        .reset_index()
    )

    # Merge to Include Team Names (Assume df_teams has 'team_id' and 'team_name')
    team_stats_by_round = pd.merge(
        team_stats_by_round,
        df_teams[['team_id', 'team_name']].drop_duplicates(),
        on='team_id',
        how='left'
    )

    # Plotly Express Line Chart
    fig = px.line(
        team_stats_by_round,
        x='round',
        y=selected_stat,
        color='team_name',
        title=f"{selected_stat.title()} by Round for Teams in {selected_season}",
        labels={'round': 'Round', selected_stat: selected_stat.title()},
        hover_data={'round': True, selected_stat: True, 'team_name': True}
    )

    # Update layout to enable interactivity
    fig.update_layout(
        legend_title_text='Teams',
        xaxis_title="Round",
        yaxis_title=f"{selected_stat.title()}",
        template="plotly_white",
        legend=dict(
            title="Teams",
            orientation="v",
            itemclick="toggle",  # Enable toggling on legend
            itemdoubleclick="toggleothers"  # Double-click isolates a team
        )
    )

    # Show the chart in Streamlit
    st.plotly_chart(fig, use_container_width=True)

    st.write("Unselect or Select a team to show in the chart by clicking on its name on the legend")