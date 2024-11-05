import os
from dotenv import load_dotenv
from helpers.SpotifyAPI import *
import pandas as pd
import streamlit as st
import time
import plotly.express as px
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from helpers.file_helper import save_recommendations_to_file, load_recommendations_from_file

TEMP_FILE_PATH = "./data/spotify_api_user_top_songs.json"
TYPES_OF_FEATURES = (
    "acousticness", 
    "danceability", 
    "duration_ms", 
    "energy", 
    "instrumentalness", 
    "mode",
    "liveness", 
    "loudness", 
    "speechiness", 
    "tempo", 
    "valence"
)

load_dotenv()
client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# get artist songs from spotify api
def spotipy_get():

    st.title("Spotify API User Profile Analysis")
    
    cooldown_period = 60    
    current_time = time.time()
    if 'last_pressed' not in st.session_state:
        st.session_state.last_pressed = 0
    if 'data' not in st.session_state:
        st.session_state.data = load_recommendations_from_file(TEMP_FILE_PATH)
        
    search_artist_button = st.button("Get My Top Tracks")
    if search_artist_button:
        time_elapsed = current_time - st.session_state.last_pressed
        if time_elapsed < cooldown_period:
            st.warning(f"Please wait {int(cooldown_period - time_elapsed)} seconds before searching again.")
        else:
            st.session_state.last_pressed = current_time
            data = sp.current_user_top_tracks(limit=20)
            st.session_state.data = data
            save_recommendations_to_file(TEMP_FILE_PATH, data)
            spotipy_all_categories(st.session_state.data, TYPES_OF_FEATURES)

    if 'data' in st.session_state and st.session_state.data:
        st.write(f"Here are some of your top tracks:")
        st.session_state.data = load_recommendations_from_file(TEMP_FILE_PATH)
        st.table(st.session_state.data)
        # Name_of_Feat = st.selectbox("Feature", TYPES_OF_FEATURES)
        # categorize = st.button("Categorize")
        # if categorize:
        #     st.table(st.session_state.data)

def spotipy_all_categories(data, TYPES_OF_FEATURES):
    need = []
    for i, item in enumerate(data['tracks']['items']):
        track = item['album']
        track_id = item['id']
        song_name = item['name']
        popularity = item['popularity']
        need.append((
            i, 
            track['artists'][0]['name'], 
            track['name'], 
            track_id, 
            song_name, 
            track['release_date'], 
            popularity
        ))
    
    df = pd.DataFrame(need, index=None, columns=["Index", "Artist", "Track", "Track ID", "Song Name", "Release Date", "Popularity"])
    
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    all_feat_df = pd.DataFrame()
    for i, item in enumerate(data['tracks']['items']):
        track_id = item['id']
        audio_features = sp.audio_features(track_id)[0]
        couples = {}
        for feature in TYPES_OF_FEATURES:
            couples[feature] = audio_features.get(feature)
        
        all_feat_df = all_feat_df.append(couples, ignore_index=True)
        
    df = pd.merge(df, all_feat_df, left_index=True, right_index=True)
    df = df.drop(columns=['Index', 'Track ID', 'Release Date'])
    
    df_dict = df.to_dict(orient='records')
    save_recommendations_to_file(TEMP_FILE_PATH, df_dict)
    
    
    
    
    