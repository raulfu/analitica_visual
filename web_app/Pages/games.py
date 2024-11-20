from utils.helpers import df_header

import matplotlib.pyplot as plt

first_game = df_header.iloc[0]

# Extract the first game's cumulative scores per quarter for both teams
quarters = ['score_quarter_1', 'score_quarter_2', 'score_quarter_3', 'score_quarter_4']

# Cumulative scores for Team A and Team B
cumulative_team_a = [first_game[f"{q}_a"] for q in quarters]
cumulative_team_b = [first_game[f"{q}_b"] for q in quarters]

# Compute points scored per quarter
points_team_a = [cumulative_team_a[0]] + [cumulative_team_a[i] - cumulative_team_a[i-1] for i in range(1, len(cumulative_team_a))]
points_team_b = [cumulative_team_b[0]] + [cumulative_team_b[i] - cumulative_team_b[i-1] for i in range(1, len(cumulative_team_b))]

# Define quarter labels
labels = ['Q1', 'Q2', 'Q3', 'Q4']

# Create a figure with 2 subplots
plt.figure(figsize=(14, 6))

# Subplot 1: Points scored per quarter
plt.subplot(1, 2, 1)
x = range(len(labels))
width = 0.4
plt.bar([p - width/2 for p in x], points_team_a, width=width, label='Team A', color='red')
plt.bar([p + width/2 for p in x], points_team_b, width=width, label='Team B', color='blue')
plt.xticks(x, labels)
plt.title('Points Scored Per Quarter', fontsize=16)
plt.xlabel('Quarter', fontsize=14)
plt.ylabel('Points', fontsize=14)
plt.legend()
plt.grid(axis='y', alpha=0.3)

# Subplot 2: Cumulative scores per quarter
plt.subplot(1, 2, 2)
plt.bar([p - width/2 for p in x], cumulative_team_a, width=width, label='Team A', color='red')
plt.bar([p + width/2 for p in x], cumulative_team_b, width=width, label='Team B', color='blue')
plt.xticks(x, labels)
plt.title('Cumulative Scores Per Quarter', fontsize=16)
plt.xlabel('Quarter', fontsize=14)
plt.ylabel('Cumulative Points', fontsize=14)
plt.legend()
plt.grid(axis='y', alpha=0.3)

# Adjust layout and display the plots
plt.tight_layout()
plt.show()
