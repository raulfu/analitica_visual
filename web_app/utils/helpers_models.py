import pandas as pd
import pickle
from utils.helpers import df_box_score, df_teams, df_box_score_eurocup
from sklearn.model_selection import train_test_split

#models
#@st.cache_data
# Load the models

#if executing locally, must add "../" to eh path. e.g. '../datasets/euroleague_players.csv'. This is due to a deployment problem with streamlit

with open('logistic_model.pkl', 'rb') as f:
    logistic_model = pickle.load(f)

with open('rf_model.pkl', 'rb') as f:
    rf_model = pickle.load(f)

with open('linear_regressor_points.pkl', 'rb') as f:
    linear_regressor = pickle.load(f)

with open('gradient_boosting_points.pkl', 'rb') as f:
    gb_regressor = pickle.load(f)

with open('svr_regressor_points.pkl', 'rb') as f:
    svr_regressor = pickle.load(f)




#creation of dataset for predictive models

df_team_stats_each_game = df_box_score[df_box_score['dorsal'] == 'TOTAL']

# Add the points_received column
df_team_stats_each_game['points_received'] = df_team_stats_each_game.groupby('game_id')['points'].shift(-1)

# To ensure the last row in each game_id group gets its corresponding points
df_team_stats_each_game['points_received'] = df_team_stats_each_game['points_received'].fillna(df_team_stats_each_game.groupby('game_id')['points'].shift(1))

# Adding column WIN
df_team_stats_each_game['win'] = (df_team_stats_each_game['points'] > df_team_stats_each_game['points_received']).astype(int)


# Add 'points_received_per_game' to df_teams
# Filter only team stats from df_team_stats_each_game
team_stats = df_team_stats_each_game[['team_id', 'season_code', 'points_received']]

# Group by team and season to calculate the mean points received
points_received_avg = team_stats.groupby(['team_id', 'season_code'])['points_received'].mean().reset_index()
points_received_avg.rename(columns={'points_received': 'points_received_per_game'}, inplace=True)

# Merge with df_teams
df_teams = pd.merge(df_teams, points_received_avg, on=['team_id', 'season_code'], how='left')

# Step 1.1: Drop unnecessary columns
columns_to_drop = ['game_player_id', 'player_id', 'is_starter', 'is_playing', 'dorsal', 'player', 'minutes']
df_team_stats_each_game = df_team_stats_each_game.drop(columns=columns_to_drop)

# Step 1.3: Combine rows into single rows representing matchups
# Split rows into two groups (team A and team B stats)
team_a_stats = df_team_stats_each_game[df_team_stats_each_game['game_id'].duplicated(keep='first')]
team_b_stats = df_team_stats_each_game[df_team_stats_each_game['game_id'].duplicated(keep='last')]

# Merge team A and team B stats into a single row per game
merged_df_team_stats_each_game = pd.merge(team_a_stats, team_b_stats, on='game_id', suffixes=('_a', '_b'))

# Optional: Remove duplicate columns and reorder if necessary
merged_df_team_stats_each_game = merged_df_team_stats_each_game.drop(columns=['game_b', 'round_b', 'phase_b'])
merged_df_team_stats_each_game.rename(columns={'season_code_a': 'season_code'}, inplace=True)
merged_df_team_stats_each_game.rename(columns={'game_a': 'game'}, inplace=True)
merged_df_team_stats_each_game.rename(columns={'round_a': 'round'}, inplace=True)
merged_df_team_stats_each_game.rename(columns={'phase_a': 'phase'}, inplace=True)


#eurocup

df_team_stats_each_game_eurocup = df_box_score_eurocup[df_box_score_eurocup['dorsal'] == 'TOTAL']

# Add the points_received column
df_team_stats_each_game_eurocup['points_received'] = df_team_stats_each_game_eurocup.groupby('game_id')['points'].shift(-1)

# To ensure the last row in each game_id group gets its corresponding points
df_team_stats_each_game_eurocup['points_received'] = df_team_stats_each_game_eurocup['points_received'].fillna(df_team_stats_each_game_eurocup.groupby('game_id')['points'].shift(1))

# Adding column WIN
df_team_stats_each_game_eurocup['win'] = (df_team_stats_each_game_eurocup['points'] > df_team_stats_each_game_eurocup['points_received']).astype(int)

# Step 1.1: Drop unnecessary columns
columns_to_drop = ['game_player_id', 'player_id', 'is_starter', 'is_playing', 'dorsal', 'player', 'minutes']
df_team_stats_each_game_eurocup = df_team_stats_each_game_eurocup.drop(columns=columns_to_drop)

# Step 1.3: Combine rows into single rows representing matchups
# Split rows into two groups (team A and team B stats)
team_a_stats_eurocup = df_team_stats_each_game_eurocup[df_team_stats_each_game_eurocup['game_id'].duplicated(keep='first')]
team_b_stats_eurocup = df_team_stats_each_game_eurocup[df_team_stats_each_game_eurocup['game_id'].duplicated(keep='last')]

# Merge team A and team B stats into a single row per game
merged_df_team_stats_each_game_eurocup = pd.merge(team_a_stats_eurocup, team_b_stats_eurocup, on='game_id', suffixes=('_a', '_b'))

# Optional: Remove duplicate columns and reorder if necessary
merged_df_team_stats_each_game_eurocup = merged_df_team_stats_each_game_eurocup.drop(columns=['game_b', 'round_b', 'phase_b'])
merged_df_team_stats_each_game_eurocup.rename(columns={'season_code_a': 'season_code'}, inplace=True)
merged_df_team_stats_each_game_eurocup.rename(columns={'game_a': 'game'}, inplace=True)
merged_df_team_stats_each_game_eurocup.rename(columns={'round_a': 'round'}, inplace=True)
merged_df_team_stats_each_game_eurocup.rename(columns={'phase_a': 'phase'}, inplace=True)

merged_df_team_stats_each_game_all_games = pd.concat([merged_df_team_stats_each_game_eurocup, merged_df_team_stats_each_game], axis=0,  ignore_index=True)




#X_train, test, etc

# Define features for both teams
features = [
    'defensive_rebounds_a', 'offensive_rebounds_a', 'assists_a',
    'three_points_made_a', 'turnovers_a', 'blocks_favour_a', 'steals_a',
    'defensive_rebounds_b', 'offensive_rebounds_b', 'assists_b',
    'three_points_made_b', 'turnovers_b', 'blocks_favour_b', 'steals_b']

# Targets
targets = ['points_a', 'points_b']
target = 'win_a'

# Input features and targets
X = merged_df_team_stats_each_game[features]
y = merged_df_team_stats_each_game[targets]
X_all = merged_df_team_stats_each_game_all_games[features]
y_all = merged_df_team_stats_each_game_all_games[target]

# Step 3.3: Train-test split
X_train_all, X_test_all, y_train_all, y_test_all = train_test_split(X_all, y_all, test_size=0.2, random_state=42)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)




# hago X_test_games_id para cuadrarlo luego en local explainabiluty de cada partido
features_ = [
    'defensive_rebounds_a', 'offensive_rebounds_a', 'assists_a',
    'three_points_made_a', 'turnovers_a', 'blocks_favour_a', 'steals_a',
    'defensive_rebounds_b', 'offensive_rebounds_b', 'assists_b',
    'three_points_made_b', 'turnovers_b', 'blocks_favour_b', 'steals_b', 'game_id']
X_games_id = merged_df_team_stats_each_game[features_]
X_train_games_id, X_test_games_id, y_train_games_id, y_test_games_id = train_test_split(X_games_id, y, test_size=0.2, random_state=42)

