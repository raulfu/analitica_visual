# EUROLEAGUE PROJECT

Project to visualize and predict how the Euroleague basketball league behaves. It includes an initial Exploratory Data Analysis of the datasets. There are tools in Streamlit to view all type of historical stats, for individuals, teams, season, etc. Including a game and season predictor for the 2024-2025, along with a section with explainability of the predictors using SHAP library. Finally, some dashboards in Tableau with relevant insights of the league.

## Setting up the environment

### 0. Prerequisites

Recommended to have the version of python 3.12.6. Upper versions may not work properly. If you are using Windows as operative system, you may download the [Windows Installer (64-bit)](https://www.python.org/ftp/python/3.12.6/python-3.12.6-amd64.exe) executable, if you are using MacOS, you may download the [macOS 64-bit universal2 installer](https://www.python.org/ftp/python/3.12.6/python-3.12.6-macos11.pkg) version. For other operative systems or specific versions, checkout the [release page](https://www.python.org/downloads/release/python-3126/) of the python version.


**Important**: Make sure to check the box **"Add Python 3.12 to PATH"** during the installation process.


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

