import os
from dotenv import load_dotenv
import requests
from helpers.SpotifyAPI import *
import pandas as pd
import streamlit as st
import time
import plotly.express as px
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from helpers.file_helper import save_recommendations_to_file, load_recommendations_from_file

TEMP_FILE_PATH = "./data/spotify_api_artist_search.json"

load_dotenv()
client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")

# get artist songs from spotify api
def spotipy_get():
    Types_of_Features = (
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

    st.title("Spotify API artist Analysis")
    
    spotify = SpotifyAPI(client_id, client_secret)
    cooldown_period = 60
    
    artist_name = st.text_input("Artist Name")
    search_artist_button = st.button("Search Artist")
    
    current_time = time.time()
    if 'last_pressed' not in st.session_state:
        st.session_state.last_pressed = 0
    if 'data' not in st.session_state:
        st.session_state.data = load_recommendations_from_file(TEMP_FILE_PATH)
        
    if search_artist_button:
        time_elapsed = current_time - st.session_state.last_pressed
        if time_elapsed < cooldown_period:
            st.warning(f"Please wait {int(cooldown_period - time_elapsed)} seconds before searching again.")
        else:
            st.session_state.last_pressed = current_time
            data = spotify.search({"artist": f"{artist_name}"}, search_type="track", limit=5)
            st.session_state.data = data
            save_recommendations_to_file(TEMP_FILE_PATH, data)
        
    if 'data' in st.session_state and st.session_state.data:
        st.write(f"Here are some tracks for you based on the artist {artist_name}:")
        Name_of_Feat = st.selectbox("Feature", Types_of_Features)
        categorize = st.button("Categorize")
        if categorize:
            spotipy_categorize(st.session_state.data, Name_of_Feat)  

# get the categorization of the data
def spotipy_categorize(data, Name_of_Feat):
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

    feat_df = pd.DataFrame()
    for i, item in enumerate(data['tracks']['items']):
        track_id = item['id']
        features = sp.audio_features([track_id])
        for feature_score, feature_name in zip(features[0].values(), features[0].keys()):
            if feature_name == Name_of_Feat:
                new_row = pd.DataFrame({
                    "Index": [i],
                    "Feature": [feature_score]
                })

                feat_df = pd.concat([feat_df, new_row], ignore_index=True)
    df = pd.merge(df, feat_df, on="Index")
    df = df[["Index", "Feature", "Popularity", "Song Name", "Artist", "Track", "Release Date"]]
    df.sort_values(by="Feature", inplace=True, ascending=False)
    
    df_dict = df.to_dict(orient='records')
    save_recommendations_to_file(TEMP_FILE_PATH, df_dict)
    
    feat_header = Name_of_Feat.capitalize()
    st.header(f'{feat_header} vs. Popularity')

    fig = px.scatter(
        df,
        x='Popularity',
        y='Feature',
        color='Feature',
        size='Popularity',
        hover_data=['Popularity', 'Feature', 'Song Name', 'Artist', 'Track'],
        title=f'{feat_header} vs. Popularity'
    )

    st.plotly_chart(fig, use_container_width=True)

    st.header("Table of Attributes")
    st.table(df)
