import spotipy
from spotipy.oauth2 import SpotifyOAuth

username = '31lim2ii6s23jjdsdmdcjgdxpyey'
SCOPE = 'user-read-recently-played user-read-private'
auth_man = spotipy.SpotifyOAuth(username=username, scope=SCOPE)
sp = spotipy.Spotify(auth_manager=auth_man)


def recently_played(played=None, limit=30):
    if played is None:
        played = []
    results = sp.current_user_recently_played(limit=limit)
    for i, item in enumerate(results['items']):
        song = item['track']
        song_name = song['name']
        song_id = song['id']
        artist_info = song['artists'][0]
        artist_name = artist_info['name']
        artist_id = artist_info['id']
        song_info = [song_id, song_name, artist_id, artist_name]
        played.append(song_info)
    return played


def search_song(name: str, limit=5):
    results = sp.search(q=name, type='track', limit=limit)
    results = results['tracks']['items'][0]
    song_name = results['name']
    song_id = results['id']
    artist_info = results['artists'][0]
    artist_name = artist_info['name']
    artist_id = artist_info['id']
    song_info = [song_id, song_name, artist_id, artist_name]
    return song_info


print(search_song('Want U Back'))
