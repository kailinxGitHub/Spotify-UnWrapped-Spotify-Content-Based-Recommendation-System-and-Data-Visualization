import os 
from dotenv import load_dotenv
import pandas as pd
import streamlit as st
import time
import plotly.express as px
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials

load_dotenv()
client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")
redirect_uri = os.getenv("SPOTIPY_REDIRECT_URI")
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id
                                               client_secret=client_secret,
                                               redirect_uri="YOUR_APP_REDIRECT_URI",
                                               scope="user-library-read"))

results = sp.current_user_saved_tracks()
print(data)