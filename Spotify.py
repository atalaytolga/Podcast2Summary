import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import re
import os

# Load environment variables from .env
load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")


client_credentials_manager = SpotifyClientCredentials(
    client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET
)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_podcast_episodes(show_id):
    """Fetch podcast episodes from a given Spotify show ID."""
    results = sp.show_episodes(show_id, limit=5)  # Get latest 5 episodes
    episodes = []

    for episode in results["items"]:
        episodes.append({
            "name": episode["name"],
            "description": episode["description"],
            "release_date": episode["release_date"],    
            "audio_preview_url": episode["audio_preview_url"],  # Preview only
            "external_url": episode["external_urls"]["spotify"]
        })

    return episodes


def extract_show_id(spotify_url):
    """Extracts Spotify show ID from URL."""
    match = re.search(r"show/([a-zA-Z0-9]+)", spotify_url)
    return match.group(1) if match else None
