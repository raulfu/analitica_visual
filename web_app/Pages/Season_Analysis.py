import streamlit as st
import pandas as pd
import altair as alt
# Team Analysis
import plotly.express as px
import pandas as pd
from utils.helpers import df_players, df_teams, df_box_score

# Streamlit Page Title
st.title("Season Analysis: Player and Team Performance")

# Sidebar for Inputs
st.sidebar.header("Filter Options")

# Radio Button for Analysis Type
analysis_type = st.sidebar.radio("Select Analysis Type", ("Player Analysis", "Team Analysis"))

# Common Inputs: Season and Statistic
seasons = df_players['season_code'].unique()
selected_season = st.sidebar.selectbox("Select Season", sorted(seasons), index=len(seasons) - 1)

statistics = [
    'points', 'total_rebounds', 'assists', 'steals', 'turnovers', 'blocks_favour',
    'blocks_against', 'valuation', 'plus_minus'
]
selected_stat = st.sidebar.selectbox("Select Statistic", statistics, index=7)

# Player Analysis
if analysis_type == "Player Analysis":
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

# Team Analysis
elif analysis_type == "Team Analysis":
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