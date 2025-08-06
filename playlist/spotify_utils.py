import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from django.conf import settings

def get_spotify_tracks_by_mood(mood, language):
    auth_manager = SpotifyClientCredentials(
        client_id=settings.SPOTIFY_CLIENT_ID,
        client_secret=settings.SPOTIFY_CLIENT_SECRET
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)
    query = f"{mood} {language} music"
    results = sp.search(q=query + " music", type='track', limit=12)
    tracks = results.get('tracks', {}).get('items', [])

    return [
        {
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'album_image': track['album']['images'][0]['url'] if track['album']['images'] else None,
            'preview_url': track['preview_url'],  # 30 sec audio clip or None
            'url': track['external_urls']['spotify'],
            'embed_url': f"https://open.spotify.com/embed/track/{track['id']}"
        }
        for track in tracks
    ]
