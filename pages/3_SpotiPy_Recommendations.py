import streamlit as st
from components.spotipy_recommendation import render_recommendations

# configures the page
st.set_page_config(
    page_title="SpotiPy Recommendations", 
    page_icon=":thumbsup:", 
    layout="centered"
)

# main content
st.title("Recommendations")
render_recommendations()