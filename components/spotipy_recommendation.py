import streamlit as st
import os
import json
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time
from helpers.file_helper import save_recommendations_to_file, load_recommendations_from_file

TEMP_FILE_PATH = "./data/temp_recommendations.json"

# keys for the spotipy API
load_dotenv()
client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# fetches the recommendation from the SpotiPy API
def get_recommendations(track_name, limit=5):
    results = sp.search(q=track_name, type='track')
    track_uri = results['tracks']['items'][0]['uri']
    recommendations = sp.recommendations(seed_tracks=[track_uri], limit=limit)['tracks']
    return recommendations

# renders the recommendations onto the page
def render_recommendations():
    st.write("Get song recommendations based on your favorite track.")
    
    cooldown_period = 60

    track_name = st.text_input("Enter a song that you like:")
    num_recommendations = st.number_input("Number of recommendations:", min_value=1, max_value=20, value=5)
    generate_song_button = st.button("Generate Recommendations")

    current_time = time.time()
    if 'last_pressed' not in st.session_state:
        st.session_state.last_pressed = 0

    recommendations = load_recommendations_from_file(TEMP_FILE_PATH)

    if generate_song_button:
        time_elapsed = current_time - st.session_state.last_pressed
        if time_elapsed < cooldown_period and recommendations:
            st.warning(f"Please wait {int(cooldown_period - time_elapsed)} seconds before generating recommendations again.")
        else:
            st.session_state.last_pressed = current_time
            recommendations = get_recommendations(track_name, limit=num_recommendations)
            save_recommendations_to_file(TEMP_FILE_PATH, recommendations)

    if recommendations:
        st.write(f"Here are some recommendations for you based on the keyword {track_name}:")
        for track in recommendations:
            st.write(f"{track['name']} by {track['album']['artists'][0]['name']}")
            href = track['album']['external_urls']['spotify']
            st.link_button(f"Listen on Spotify", href)
            st.image(track['album']['images'][0]['url'])