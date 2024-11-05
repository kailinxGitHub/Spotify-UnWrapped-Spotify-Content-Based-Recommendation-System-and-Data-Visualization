import streamlit as st
import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time

load_dotenv()
client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_recommendations(track_name, limit=5):
    results = sp.search(q=track_name, type='track')
    track_uri = results['tracks']['items'][0]['uri']

    recommendations = sp.recommendations(seed_tracks=[track_uri], limit=limit)['tracks']
    return recommendations
        
def render_recommendations():
    st.write("Here are some recommendations for you using SpotiPy's recommendation API.")
    if 'last_pressed' not in st.session_state:
        st.session_state.last_pressed = 0
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = []

    # Cooldown period in seconds
    cooldown_period = 60

    track_name = st.text_input("Enter a song that you like:")
    num_recommendations = st.number_input("Number of recommendations:", min_value=1, max_value=20, value=5)
    generate_song_button = st.button("Generate Recommendations")

    current_time = time.time()

    if generate_song_button:
        time_elapsed = current_time - st.session_state.last_pressed
        if time_elapsed < cooldown_period and st.session_state.recommendations != []:
            st.warning(f"Please wait {int(cooldown_period - time_elapsed)} seconds before generating recommendations again.")
        else:
            st.session_state.last_pressed = current_time
            st.session_state.recommendations = get_recommendations(track_name, limit=num_recommendations)

    if st.session_state.recommendations:
        for track in st.session_state.recommendations:
            st.write(f"{track['name']} by {track['album']['artists'][0]['name']}")
            href = track['album']['external_urls']['spotify']
            st.link_button(f"Listen on Spotify", href)
            st.image(track['album']['images'][0]['url'])