import streamlit as st
from components.spotify_api_artist_analysis import spotipy_get

# configures the page
st.set_page_config(
    page_title="Artist Analysis", 
    page_icon=":thinking_face:", 
    layout="centered"
)

# main content
spotipy_get()