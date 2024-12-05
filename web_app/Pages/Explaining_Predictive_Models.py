import streamlit as st
import numpy as np
import shap
import matplotlib.pyplot as plt
import pandas as pd
from utils.helpers_models import linear_regressor, logistic_model, X_test, X_train, X_test_all, X_train_all, X_test_games_id
from utils.helpers import df_header



def Explaining_Predictions_main():

    shap.initjs()


    # SHAP Explainer for MultiOutputRegressor
    explainer_points_a = shap.Explainer(linear_regressor.estimators_[1], X_train)
    explainer_points_b = shap.Explainer(linear_regressor.estimators_[0], X_train)
    # Compute SHAP values for each target
    shap_values_points_a = explainer_points_a(X_test)
    shap_values_points_b = explainer_points_b(X_test)


    # SHAP Explainer for Logistic Regression model
    explainer = shap.Explainer(logistic_model, X_train_all)
    shap_values = explainer(X_test_all)
    predicted_probabilities = logistic_model.predict_proba(X_test_all)[:, 1]
    average_prediction = np.mean(predicted_probabilities)


    # cosas streamlit 
    st.title("Explainability of Predictive Model On The Outcome Of a Euroleague Basketball Game")
    option = st.sidebar.radio("Select Explainability Type", ("Global", "Local"))


    if option == "Global":


        st.header("Global Explainability")
        st.write("## Understand how the model behaves across all predictions.")


        model_selected = st.radio("Select Model To Explain", ("Logistic (Simple - Who Wins?)", "Linear Regressor (How Many Points?)"), index=1)


        if model_selected == "Logistic (Simple - Who Wins?)":

            st.write("## Logistic Model For Who Wins")

            #st.write(f"#### The average prediction for all games (target is local team wins) is: {average_prediction:.4f}")

            # SHAP Summary Plot
            st.write("### SHAP Summary Plot")
            fig_summary, ax = plt.subplots()
            shap.summary_plot(shap_values, X_test_all, show=False)
            st.pyplot(fig_summary)

            # SHAP Bar Plot
            st.write("### SHAP Bar Plot (Top Features)")
            fig_bar, ax = plt.subplots()
            shap.plots.bar(shap_values, show=False)
            st.pyplot(fig_bar)

            # SHAP Scatter Plots
            st.write("### Feature Interaction: DEFENSIVE REBOUNDS (local team) vs. THREE POINTS MADE (away team)")
            fig_age_heart, ax = plt.subplots()
            shap.plots.scatter(shap_values[:, 'defensive_rebounds_a'], color=shap_values[:, 'three_points_made_b'], ax=ax)
            st.pyplot(fig_age_heart)


        else:

            st.write("## Linear Regressor For Points Scored")

            col3, col4 = st.columns(2)

            with col3:

                st.write("### SHAP Summary Plot Points Local")
                fig_summary, ax = plt.subplots()
                shap.summary_plot(shap_values_points_a, X_test, show=False)
                st.pyplot(fig_summary)

                st.write("### SHAP Bar Plot (Top Features Local)")
                fig_bar, ax = plt.subplots()
                shap.plots.bar(shap_values_points_a, show=False)
                st.pyplot(fig_bar)

                st.write("### Local Explainer Feature Interaction: DEFENSIVE REBOUNDS (local team) vs. THREE POINTS MADE (away team)")
                fig_age_heart, ax = plt.subplots()
                shap.plots.scatter(shap_values_points_a[:, 'defensive_rebounds_a'], color=shap_values_points_a[:, 'three_points_made_b'], ax=ax)
                st.pyplot(fig_age_heart)


            with col4:

                st.write("### SHAP Summary Plot Points Away")
                fig_summary, ax = plt.subplots()
                shap.summary_plot(shap_values_points_b, X_test, show=False)
                st.pyplot(fig_summary)

                st.write("### SHAP Bar Plot (Top Features Away)")
                fig_bar, ax = plt.subplots()
                shap.plots.bar(shap_values_points_a, show=False)
                st.pyplot(fig_bar)

                st.write("### Away Explainer Feature Interaction: DEFENSIVE REBOUNDS (local team) vs. THREE POINTS MADE (away team)")
                fig_age_heart, ax = plt.subplots()
                shap.plots.scatter(shap_values_points_b[:, 'defensive_rebounds_a'], color=shap_values_points_b[:, 'three_points_made_b'], ax=ax)
                st.pyplot(fig_age_heart)


    elif option == "Local":

        st.header("Local Explainability")
        st.write("### Understand and interpret specific predictions for any game.")

        selected_game_id_slider = st.selectbox("Select a Game", X_test_games_id['game_id'])
        selected_game = df_header[df_header['game_id'] == selected_game_id_slider].iloc[0]
        st.write(f"#### REAL SCORE: {selected_game['team_a']} {selected_game['score_a']} vs {selected_game['score_b']} {selected_game['team_b']} ({selected_game['phase']} GAME ON {selected_game['season_code']} SEASON ON {selected_game['date']})")
        
        sample_X = X_test_games_id[X_test_games_id['game_id'] == selected_game_id_slider]
        
        try:

            sample_X = sample_X.drop('game_id', axis=1)

            model_selected = st.radio("Select Model To Explain", ("Logistic (Simple - Who Wins?)", "Linear Regressor (How Many Points?)"), index=1)


            if model_selected == "Logistic (Simple - Who Wins?)":
                
                # --- Logistic Regression Explainability ---
                st.subheader("Logistic Model (Who Wins?)")
                #st.write(f"#### If lines go left (negative result f(x)) means that local team wins. If lines go right means away team wins.")

                shap_values_sample = explainer(sample_X)

                st.write("### Waterfall Plot for Logistic Model Prediction")
                fig_waterfall_logistic, ax = plt.subplots()
                shap.plots.waterfall(shap_values_sample[0])
                st.pyplot(fig_waterfall_logistic)

                st.write("### Decision Plot for Logistic Model Prediction")
                fig_decision_logistic, ax = plt.subplots()
                shap.decision_plot(explainer.expected_value, shap_values_sample.values[0], feature_names=list(X_test_all.columns))
                st.pyplot(fig_decision_logistic)

            else:
            
                # --- Linear Regression Explainability ---
                st.subheader("Linear Regression Model (Points Scored)")
                st.write(f"#### Points scored by each team is f(x)")

                col3, col4 = st.columns(2)

                with col3:
                
                    # Points_a (local team)
                    st.write(f"### Local Team: {selected_game['team_a']} (Points Scored)")
                    shap_values_points_a_sample = explainer_points_a(sample_X)

                    st.write("### Waterfall Plot for Points Scored by Local Team")
                    fig_waterfall_points_a, ax = plt.subplots()
                    shap.plots.waterfall(shap_values_points_a_sample[0])
                    st.pyplot(fig_waterfall_points_a)

                    st.write("### Decision Plot for Points Scored by Local Team")
                    fig_decision_points_a, ax = plt.subplots()
                    shap.decision_plot(explainer_points_a.expected_value, shap_values_points_a_sample.values[0], feature_names=list(X_test.columns))
                    st.pyplot(fig_decision_points_a)

                with col4:
                        
                    # Points_b (away team)
                    st.write(f"### Away Team: {selected_game['team_b']} (Points Scored)")
                    shap_values_points_b_sample = explainer_points_b(sample_X)

                    st.write("### Waterfall Plot for Points Scored by Away Team")
                    fig_waterfall_points_b, ax = plt.subplots()
                    shap.plots.waterfall(shap_values_points_b_sample[0])
                    st.pyplot(fig_waterfall_points_b)

                    st.write("### Decision Plot for Points Scored by Away Team")
                    fig_decision_points_b, ax = plt.subplots()
                    shap.decision_plot(explainer_points_b.expected_value, shap_values_points_b_sample.values[0], feature_names=list(X_test.columns))
                    st.pyplot(fig_decision_points_b)


        except IndexError:
            st.write('Game not in test dataset')
        




if __name__ == "__main__":
    main()