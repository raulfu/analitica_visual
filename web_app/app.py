import streamlit as st

from Pages.Explaining_Predictive_Models import Explaining_Predictions_main
from Pages.Games_Analysis import Games_Analysis_main
from Pages.Players_Season_Analysis import Players_Season_Analysis_main
from Pages.Players_Tops import Players_Tops_main
from Pages.Predicting_Outcome_Of_A_Game import Predicting_Outcome_Of_A_Game_main
from Pages.Predicting_Teams_Records import Predicting_Teams_Records_main
from Pages.Teams_Season_Analysis import Teams_Season_Analysis_main
from Pages.Teams_Tops import Teams_Tops_main


#cd Desktop\analitica_visual\final_project\analitica_visual\web_app
#streamlit run app.py



st.set_page_config(page_title="Euroleague Basketball Analytics", page_icon=":basketball:", layout="wide", initial_sidebar_state="auto")



def main():
    st.title("EUROLEAGUE BASKETBALL ANALYTICS")
    st.subheader("Raúl Fuente - Oscar Colom")

    st.write("### This is a web-app where one can explore Euroleague basketball history since 2007 until the last games played in the 4/12/2024")
    st.write("#### The web has 3 sections that include:\n"
            "- Season Analysis: see how players and teams perform in a givem season, as well as seeing an specific game statostics\n"
            "- Tops: search for the top you want for players or teams. choose the statistic you want, the number of players to show or the season/history.\n"
            "- Predictions: various prediction models are given to either predict the outcome of a game of this current season, or the points each team will score."
            "Using our linear regressor model we also predict the given team record of this season. One can also understand how models work in the explainability part.")



def setup_pages():

    # -- Pages Setup --
    main_page = st.Page(main, title="Home", icon=":material/home:", default=True)

    Explaining_Predictions_page = st.Page(Explaining_Predictions_main, title="Explaining Predictions", icon=":material/smart_toy:")

    Games_Analysis_page = st.Page(Games_Analysis_main, title="Games", icon=":material/calendar_today:")

    Players_Season_Analysis_page = st.Page(Players_Season_Analysis_main, title="Players", icon=":material/calendar_today:")

    Players_Tops_page = st.Page(Players_Tops_main, title="Top Players", icon=":material/insert_chart_outlined:")

    Predicting_Outcome_Of_A_Game_page = st.Page(Predicting_Outcome_Of_A_Game_main, title="Predictor: Outcome of a Game", icon=":material/smart_toy:")

    Predicting_Teams_Records_main_page = st.Page(Predicting_Teams_Records_main, title="Predictor: Team Record - Season", icon=":material/smart_toy:")

    Teams_Season_Analysis_page = st.Page(Teams_Season_Analysis_main, title="Teams", icon=":material/calendar_today:")

    Teams_Tops_page = st.Page(Teams_Tops_main, title="Top Teams", icon=":material/insert_chart_outlined:")



    # -- Navigation Setup --
    pages = st.navigation(
        {
            "": [main_page],
            "Season Analysis": [Players_Season_Analysis_page, Teams_Season_Analysis_page, Games_Analysis_page],
            "Tops": [Players_Tops_page, Teams_Tops_page],
            "Predictions": [Predicting_Outcome_Of_A_Game_page, Predicting_Teams_Records_main_page, Explaining_Predictions_page]            
        }
    )
    pages.run()


if __name__ == '__main__':
    setup_pages()

