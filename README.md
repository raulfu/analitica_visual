# EUROLEAGUE PROJECT

Project to visualize and predict how the Euroleague basketball league behaves. It includes an initial Exploratory Data Analysis of the datasets. There are tools in Streamlit to view all type of historical stats, for individuals, teams, season, etc. Including a game and season predictor for the 2024-2025, along with a section with explainability of the predictors using SHAP library. Finally, some dashboards in Tableau with relevant insights of the league.

## Setting up the environment

### 0. Prerequisites

Recommended to have the version of python 3.9.12 or 3.10. Upper versions may not work properly. 

If the repository is cloned locally, "../" needs to be added before each path on files web_app/utils/helpers.py and web_app/utils/helpers_models.py (e.g. if executed locally, add "../" to the start of each of the paths to read the CSVs -> '../datasets/euroleague_players.csv' instead of 'datasets/euroleague_players.csv' ). This format for the path encountered error when the app was being deployed.

### 1. Clone the repository
Clone our repository to your local machine using the following command:
```bash
git clone https://github.com/raulfu/analitica_visual.git
```

### 2. Install Streamlit and SHAP libraries, also make sure version of scikit-learn is 1.0.2.

### 3. Run the application
To run the application, execute the following commands when the path is in web_app folder:
```bash
streamlit run app.py
```

