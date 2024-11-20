from utils.helpers import df_header

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

first_game = df_header.iloc[0]


# Simulate the first game's data
first_game = pd.Series(data)

# Extract cumulative scores
quarters = ['score_quarter_1', 'score_quarter_2', 'score_quarter_3', 'score_quarter_4']
cumulative_team_a = [first_game[f"{q}_a"] for q in quarters]
cumulative_team_b = [first_game[f"{q}_b"] for q in quarters]

# Compute points scored per quarter
points_team_a = [cumulative_team_a[0]] + [cumulative_team_a[i] - cumulative_team_a[i-1] for i in range(1, len(cumulative_team_a))]
points_team_b = [cumulative_team_b[0]] + [cumulative_team_b[i] - cumulative_team_b[i-1] for i in range(1, len(cumulative_team_b))]

# Define quarter labels
labels = ['Q1', 'Q2', 'Q3', 'Q4']

# Streamlit application
st.title("Game Analysis")

# Points scored per quarter
st.subheader("Points Scored Per Quarter")
points_df = pd.DataFrame({
    "Quarter": labels,
    "Team A": points_team_a,
    "Team B": points_team_b
}).set_index("Quarter")
st.bar_chart(points_df)

# Cumulative scores per quarter
st.subheader("Cumulative Scores Per Quarter")
cumulative_df = pd.DataFrame({
    "Quarter": labels,
    "Team A": cumulative_team_a,
    "Team B": cumulative_team_b
}).set_index("Quarter")
st.bar_chart(cumulative_df)

# Matplotlib visualizations
st.subheader("Matplotlib Visualizations")

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Subplot 1: Points scored per quarter
x = range(len(labels))
width = 0.4
axes[0].bar([p - width/2 for p in x], points_team_a, width=width, label='Team A', color='red')
axes[0].bar([p + width/2 for p in x], points_team_b, width=width, label='Team B', color='blue')
axes[0].set_xticks(x)
axes[0].set_xticklabels(labels)
axes[0].set_title('Points Scored Per Quarter', fontsize=16)
axes[0].set_xlabel('Quarter', fontsize=14)
axes[0].set_ylabel('Points', fontsize=14)
axes[0].legend()
axes[0].grid(axis='y', alpha=0.3)

# Subplot 2: Cumulative scores per quarter
axes[1].bar([p - width/2 for p in x], cumulative_team_a, width=width, label='Team A', color='red')
axes[1].bar([p + width/2 for p in x], cumulative_team_b, width=width, label='Team B', color='blue')
axes[1].set_xticks(x)
axes[1].set_xticklabels(labels)
axes[1].set_title('Cumulative Scores Per Quarter', fontsize=16)
axes[1].set_xlabel('Quarter', fontsize=14)
axes[1].set_ylabel('Cumulative Points', fontsize=14)
axes[1].legend()
axes[1].grid(axis='y', alpha=0.3)

# Adjust layout
plt.tight_layout()
st.pyplot(fig)
