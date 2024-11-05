import streamlit as st
from components.spotify_api_user_top_analysis import spotipy_get

# configures the page
st.set_page_config(
    page_title="Your Profile Analysis", 
    page_icon=":grin:", 
    layout="centered"
)

spotipy_get()