import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import time
import datetime
import gspread
from wrapped_functions import get_track_ids, get_track_features, insert_to_gsheet
from dotenv import load_dotenv
import os

load_dotenv()
SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
SPOTIPY_REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')
SCOPE = "user-top-read"

# Authorize
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, 
                                               client_secret=SPOTIPY_CLIENT_SECRET, 
                                               redirect_uri=SPOTIPY_REDIRECT_URI, 
                                               scope=SCOPE))

# Run script to insert into sheet
time_ranges = ['short_term', 'medium_term', 'long_term']
for time_period in time_ranges:
    top_tracks = sp.current_user_top_tracks(limit=20, offset=0, time_range=time_period)
    track_ids = get_track_ids(top_tracks)
    insert_to_gsheet(track_ids, time_period)