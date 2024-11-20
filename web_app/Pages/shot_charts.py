import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Define the basketball court size (adjust as per your data's coordinate system)
court_width = 28  # Width in feet for half court (FIBA)
court_height = 15  # Height in feet for half court (FIBA)

# Function to draw the basketball court
def plot_basketball_court(ax=None):
    if ax is None:
        ax = plt.gca()

    # Set court dimensions
    ax.set_xlim(0, court_width)
    ax.set_ylim(0, court_height)
    ax.set_facecolor('lightgrey')

    # Draw the key (painted area)
    ax.add_patch(plt.Rectangle((0, 0), 8, 15, linewidth=2, edgecolor='black', facecolor='none'))

    # Draw the 3-point line (simplified for half court)
    ax.plot([0, court_width], [8, 8], color="black", linestyle="--")  # Half court line

    # Draw the hoop
    ax.add_patch(plt.Circle((court_width, 7.5), 0.5, color="orange", fill=False))

    # Draw free throw circle
    ax.add_patch(plt.Circle((8, 7.5), 2.75, color="black", fill=False))

    return ax

# Function to plot shot locations
def plot_shot_locations(df_shots):
    fig, ax = plt.subplots(figsize=(10, 6))
    plot_basketball_court(ax)

    # Plot the shots
    ax.scatter(df_shots['coord_x'], df_shots['coord_y'], color='red', alpha=0.6, label='Shots')

    # Labeling
    ax.set_title("Shot Locations")
    ax.set_xlabel("Court X (ft)")
    ax.set_ylabel("Court Y (ft)")
    ax.legend()

    return fig

# Function to plot shot heatmap
def plot_shot_heatmap(df_shots):
    fig, ax = plt.subplots(figsize=(10, 6))
    plot_basketball_court(ax)

    # Generate a heatmap
    heatmap, xedges, yedges = np.histogram2d(df_shots['coord_x'], df_shots['coord_y'], bins=30, range=[[0, court_width], [0, court_height]])
    extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]

    # Plot the heatmap
    ax.imshow(heatmap.T, extent=extent, origin='lower', cmap='hot', alpha=0.5)

    # Labeling
    ax.set_title("Shot Density Heatmap")
    ax.set_xlabel("Court X (ft)")
    ax.set_ylabel("Court Y (ft)")

    return fig

# Streamlit app
st.title("Basketball Shot Visualization")
st.write("Visualize shot locations and heatmaps on a basketball court")

# Example data: Replace this with your actual data
data = {
    'coord_x': np.random.uniform(0, court_width, 100),  # Random x-coordinates
    'coord_y': np.random.uniform(0, court_height, 100)  # Random y-coordinates
}
df_shots = pd.DataFrame(data)

# Shot locations scatter plot
st.subheader("Shot Locations")
fig_shot_locations = plot_shot_locations(df_shots)
st.pyplot(fig_shot_locations)

# Shot density heatmap
st.subheader("Shot Heatmap")
fig_shot_heatmap = plot_shot_heatmap(df_shots)
st.pyplot(fig_shot_heatmap)
