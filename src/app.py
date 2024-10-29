import os
import pandas as pd
#import seaborn as sns
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import base64
import requests
import seaborn as sns

# load the .env file variables
load_dotenv()

client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

# Encode the client credentials
client_credentials = f"{client_id}:{client_secret}"
client_credentials_base64 = base64.b64encode(client_credentials.encode())

# Prepare the token request
token_url = "https://accounts.spotify.com/api/token"
headers = {
    "Authorization": f"Basic {client_credentials_base64.decode()}"
}
data = {
    "grant_type": "client_credentials"
}

# Request access token
response = requests.post(token_url, headers=headers, data=data)

# Check if the request was successful
if response.status_code == 200:
    access_token = response.json()['access_token']
    print("Access token obtained!")
else:
    print(f"Failed to obtain access token. Status code: {response.status_code}")
    print(response.text)

artist_id = "3lFDsTyYNPQc8WzJExnQWn"

top_tracks = sp.artist_top_tracks(artist_id, country='US')

for idx, track in enumerate(top_tracks['tracks'], start=1):
     # print(f"Track data: {track}")
    track_name = track['name']
    album_name = track['album']['name']
    print(f"{idx}. {track_name} - Album: {album_name}- Popularity: {track['popularity']} - Duration: {track['duration_ms']/60000} minutes")
    
top_songs = []
for track in top_tracks['tracks'][:10]:
    song_info = {
        "name": track['name'],
        "popularity": track['popularity'],
        "duration_min": round(track['duration_ms'] / 60000, 2)  # Convert ms to minutes
    }
    top_songs.append(song_info)

top_songs_df = pd.DataFrame(top_songs)
top_songs_df.head()

scatter_plot = sns.scatterplot(data = top_songs_df, x = "popularity", y = "duration_min")
fig = scatter_plot.get_figure()
fig.savefig("scatter_plot.png")