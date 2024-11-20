import os
from dotenv import load_dotenv
import requests
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import base64
import pandas as pd
import streamlit as st
from machine_learning.Perceptron import Perceptron
from sklearn.preprocessing import MinMaxScaler
from sklearn.utils import resample

load_dotenv()
client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
features = ["Key", "Loudness", "Mode", "Speechiness", "Acousticness", "Instrumentalness", "Liveness", "Valence", "Tempo"]
top_100_data = pd.read_csv('./components/top_100_playlist_most_streamed_songs.csv')

# gets the recommendation based on the name of the track using the SpotiPy client
def get_recommendations(track_name):
    results = sp.search(q=track_name, type='track')
    track_uri = results['tracks']['items'][0]['uri']

    recommendations = sp.recommendations(seed_tracks=[track_uri])['tracks']
    return recommendations

# authenticating the user
def auth(): 
    os.getegid

    CLIENT_ID = client_id
    CLIENT_SECRET = client_secret

    client_credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
    client_credentials_base64 = base64.b64encode(client_credentials.encode())

    token_url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Authorization': f'Basic {client_credentials_base64.decode()}'
    }
    data = {
        'grant_type': 'client_credentials'
    }
    response = requests.post(token_url, data=data, headers=headers)

    if response.status_code == 200:
        access_token = response.json()['access_token']
        return access_token
        print("Access token obtained successfully.")
    else:
        print("Error obtaining access token.")
        exit()
        
# gets the trending playlist
def get_trending_playlist_data(playlist_id, access_token):
    sp = spotipy.Spotify(auth=access_token)

    playlist_tracks = sp.playlist_tracks(playlist_id, fields='items(track(id, name, artists, album(id, name)))')

    music_data = []
    for track_info in playlist_tracks['items']:
        track = track_info['track']
        track_name = track['name']
        artists = ', '.join([artist['name'] for artist in track['artists']])
        album_name = track['album']['name']
        album_id = track['album']['id']
        track_id = track['id']

        audio_features = sp.audio_features(track_id)[0] if track_id != 'Not available' else None

        try:
            album_info = sp.album(album_id) if album_id != 'Not available' else None
            release_date = album_info['release_date'] if album_info else None
        except:
            release_date = None

        try:
            track_info = sp.track(track_id) if track_id != 'Not available' else None
            popularity = track_info['popularity'] if track_info else None
        except:
            popularity = None

        track_data = {
            'Track Name': track_name,
            'Artists': artists,
            'Album Name': album_name,
            'Album ID': album_id,
            'Track ID': track_id,
            'Popularity': popularity,
            'Release Date': release_date,
            'Duration (ms)': audio_features['duration_ms'] if audio_features else None,
            'Explicit': track_info.get('explicit', None),
            'External URLs': track_info.get('external_urls', {}).get('spotify', None),
            'Danceability': audio_features['danceability'] if audio_features else None,
            'Energy': audio_features['energy'] if audio_features else None,
            'Key': audio_features['key'] if audio_features else None,
            'Loudness': audio_features['loudness'] if audio_features else None,
            'Mode': audio_features['mode'] if audio_features else None,
            'Speechiness': audio_features['speechiness'] if audio_features else None,
            'Acousticness': audio_features['acousticness'] if audio_features else None,
            'Instrumentalness': audio_features['instrumentalness'] if audio_features else None,
            'Liveness': audio_features['liveness'] if audio_features else None,
            'Valence': audio_features['valence'] if audio_features else None,
            'Tempo': audio_features['tempo'] if audio_features else None,
        }

        music_data.append(track_data)

    df = pd.DataFrame(music_data)

    return df

# uses the perceptron model to predict recommentation
def perceptron_recommendation(music_df):
    music_df["Label"] = 1
    top_100_data["Label"] = 0

    combined_data = pd.concat([music_df, top_100_data], ignore_index=True)

    features = ["Danceability", "Energy", "Valence", "Tempo", "Popularity", "Duration (ms)"]
    scaler = MinMaxScaler()
    combined_data[features] = scaler.fit_transform(combined_data[features])

    df_majority = combined_data[combined_data["Label"] == 0]
    df_minority = combined_data[combined_data["Label"] == 1]

    df_minority_upsampled = resample(
        df_minority,
        replace=True,
        n_samples=len(df_majority),
        random_state=42
    )

    balanced_data = pd.concat([df_majority, df_minority_upsampled])
    X = balanced_data[features].values
    y = balanced_data["Label"].values

    perceptron = Perceptron(features=features, learning_rate=0.01, epochs=50)
    perceptron.fit(X, y)

    all_songs_normalized = scaler.transform(top_100_data[features])
    predictions = perceptron.predict(all_songs_normalized)

    top_100_data["Recommended"] = predictions
    recommended = top_100_data[top_100_data["Recommended"] == 1]

    if len(recommended) >= 5:
        recommended_sample = recommended.sample(n=5, random_state=42)
    else:
        recommended_sample = recommended

    recommended_sample = recommended_sample[["Track Name", "Artists", "Album Name", "Popularity", "Release Date"]]
    return recommended_sample

# streamlit portion
def playlist_recommendation(playlist_id):
    access_token = auth()
    music_df = get_trending_playlist_data(playlist_id, access_token)
    
    st.write("Perceptron Recommendation:")
    recommended = perceptron_recommendation(music_df)
    st.dataframe(recommended)
    
    st.write("Full Playlist Data:")
    st.dataframe(music_df)
    
    st.write("Top 100 Playlist Data:")
    st.dataframe(top_100_data)