import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
from utils.helpers import df_header

#cd Desktop\analitica_visual\final_project\analitica_visual_project\web_app
#streamlit run my_app.py



st.title("EUROLEAGUE HOOPS ANALYTICS")
st.subheader("Raúl Fuente - Oscar Colom")

st.write("# Description")
st.write("## This is a web-app where one can explore a Euroleague basketball dataset")
st.write("### A preview of the dataset is given below. One can visualize the data or make predictions")

st.write("# Dataset Preview")
st.write(df_header.head())


