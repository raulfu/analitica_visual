import pandas as pd
import matplotlib.pyplot as plt

# datasets
df_players = pd.read_csv('../datasets/euroleague_players.csv')
df_box_score = pd.read_csv('../datasets/euroleague_box_score.csv')
df_teams = pd.read_csv('../datasets/euroleague_teams.csv')
df_points = pd.read_csv('../datasets/euroleague_points.csv')
df_header = pd.read_csv('../datasets/euroleague_header.csv')


# Define a function to create the plots with black background
def create_plot(data, title, xlabel, ylabel,color):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(data.index, data.values, color=color)
    
    # Set background color to black
    fig.patch.set_facecolor('black')
    ax.set_facecolor('black')
    
    # Set the title and labels, changing text color to white for visibility
    ax.set_title(title, color='white')
    ax.set_xlabel(xlabel, color='white')
    ax.set_ylabel(ylabel, color='white')
    
    # Change tick parameters for better readability on black background
    ax.tick_params(axis='x', rotation=45, labelcolor='white')
    ax.tick_params(axis='y', labelcolor='white')
    
    return fig

