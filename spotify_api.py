import os
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=os.getenv("SPOTIFY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIFY_CLIENT_SECRET")
    )
)

def get_songs(mood, limit=10):
    results = sp.search(q=f"{mood} songs", type="track", limit=limit)
    songs = []

    for track in results["tracks"]["items"]:
        songs.append({
            "name": track["name"],
            "artist": track["artists"][0]["name"],
            "url": track["external_urls"]["spotify"]
        })

    return songs
