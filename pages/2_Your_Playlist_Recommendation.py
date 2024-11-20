import streamlit as st
from components.spotify_playlist_analysis import playlist_recommendation
from helpers.file_helper import save_recommendations_to_file, load_recommendations_from_file
from helpers.helpers import clean_spotify_url_id
import time

st.set_page_config(
    page_title="Your Playlist Recommendation", 
    page_icon=":notes:", 
    layout="centered"
)

# main content
st.title("Spotify API Playlist Recommendation")
cooldown_period = 60

playlist_link = st.text_input("Your Playlist Link")
clean_playlist_link = clean_spotify_url_id(playlist_link)
TEMP_FILE_PATH = f"./data/{clean_playlist_link}.json"
search_recommendation_button = st.button("Get Recommendations")

# the button cooldown logic
current_time = time.time()
if 'last_pressed' not in st.session_state:
        st.session_state.last_pressed = 0
if 'data' not in st.session_state:
    st.session_state.data = load_recommendations_from_file(TEMP_FILE_PATH)
if search_recommendation_button:
    time_elapsed = current_time - st.session_state.last_pressed
    if time_elapsed < cooldown_period:
        st.warning(f"Please wait {int(cooldown_period - time_elapsed)} seconds before searching again.")
    else:
        st.session_state.last_pressed = current_time
        data = playlist_recommendation(clean_playlist_link)