import streamlit as st
from components.spotipy_recommendation import render_recommendations

st.set_page_config(
    page_title="SpotiPy Recommendations", 
    page_icon=":thumbsup:", 
    layout="centered"
)

st.title("Recommendations")
render_recommendations()