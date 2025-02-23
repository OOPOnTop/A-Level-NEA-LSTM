from typing import Dict, Union, Any
import sqlite3
import spotipy

# Global variables
SCOPE = 'user-read-recently-played user-read-private'  # What access the program has to users spotify accounts

# For testing Class functionality
"""USER_ID = 1
# Database connection and fetching
con = sqlite3.connect('GUI/Users.db')
cur = con.cursor()
username = cur.execute(SELECT spotify_username FROM user_info WHERE infoID=?, (USER_ID,)).fetchone()"""


class APICalls(spotipy.Spotify):
    """
        Class that contains all logic for making API requests and formatting them to simple arrays that can be called
        throughout the program
        Contains methods for fetching recently played songs, specific search results, song features
        """

    def __init__(self, username, limit=50):
        super().__init__()
        self.auth_manager = spotipy.SpotifyOAuth(username=username, scope=SCOPE)
        self.username = username
        self.played_info = []
        self.played_info = self.recently_played(limit)
        self.played_songs = []
        self.played_songs = self.recently_played_song_artist()
        self.recently_played_features = []

    def recently_played(self, limit=50) -> list:
        """
        Takes users recently played songs and formatted to easy accessible array
        :param limit:
        :return array:
        """
        self.played_info = []
        results = self.current_user_recently_played(limit=limit)
        for i, item in enumerate(results['items']):
            song = item['track']
            song_name = song['name']
            song_id = song['id']
            artist_info = song['artists'][0]
            artist_name = artist_info['name']
            artist_id = artist_info['id']
            song_info = [song_id, song_name, artist_id, artist_name]
            self.played_info.append(song_info)
        return self.played_info

    def recently_played_song_artist(self) -> list:
        """
        Returns artists from users recently played
        :return array:
        """
        for i in self.played_info:
            _ = [i[1], i[3]]
            self.played_songs.append(_)
        return self.played_songs

    def recently_played_song_features(self):
        """
        Returns features from users recently played
        :return:
        """
        temp_list = []
        for i in self.played_info:
            _ = [i, self.get_song_features(i[1])]
            temp_list.append(_)
        self.recently_played_features = temp_list
        return self.recently_played_features

    def get_song_features(self, name: str) -> dict[Union[str, Any], Any]:
        """
        Takes a string name to search songs and provides a dictionary with features from the song
        :param name:
        :return:
        """
        tracks = [self.search_song(name)[0]]
        all_features = self.audio_features(tracks)
        features = {'Danceability': all_features[0]['danceability'],
                    'Energy': all_features[0]['energy'],
                    "Mode": all_features[0]['mode'],
                    "Speechiness": all_features[0]['speechiness'],
                    "Acousticness": all_features[0]['acousticness'],
                    "Liveness": all_features[0]['liveness'],
                    "Valence": all_features[0]['valence'],
                    "Tempo": all_features[0]['tempo'],
                    "Duration": all_features[0]['duration_ms'],
                    "Time Signature": all_features[0]['time_signature']
                    }
        return features

    def print_song_features(self, name: str) -> any:
        features = self.get_song_features(name)
        for key in features:
            print(key, " - ", features[key])

    def search_song(self, name: str, limit=1) -> list:
        """
        API call which returns formatted results of an API call
        :param name:
        :param limit:
        :return:
        """
        results = self.search(q=name, type='track', limit=limit)
        results = results['tracks']['items'][0]
        song_name = results['name']
        song_id = results['id']
        artist_info = results['artists'][0]
        artist_name = artist_info['name']
        artist_id = artist_info['id']
        song_info = [song_id, song_name, artist_id, artist_name]
        return song_info

    def print_search_song(self, name: str) -> any:
        song_info = self.search_song(name)
        print(song_info[1], " - ", song_info[3])

    def search_bar_search(self, q: str):
        """
        Returns necessary features for search bar search
        :param q:
        :return:
        """
        results = self.search(q=q, limit=50, type='track')
        results = results['tracks']['items']
        answers = []
        for i in results:
            _ = []
            track_name = i['name']
            track_id = i['id']
            artist_name = i['artists'][0]['name']
            artist_id = i['artists'][0]['id']
            _.append(track_id)
            _.append(track_name)
            _.append(artist_id)
            _.append(artist_name)
            answers.append(_)
        return answers

    def get_recent_id(self):
        """
        Gets id's of users 5 most recently played songs
        :return:
        """
        ids = []
        recent5 = self.played_info[:1]
        for i in recent5:
            ids.append(str(i[0]))
        return tuple(ids)

    def search_by_features(self, optimal_features: list, limit=10) -> any:
        """
        Takes in an array of features and gets song recommendations of values.
        :param optimal_features: arr
        :param limit: number of suggestions
        :return: arr of song suggestions
        """
        features = {
            'Danceability': float(optimal_features[0][0]),
            'Energy': float(optimal_features[1][0]),
            'Mode': int(optimal_features[2][0]),
            'Speechiness': float(optimal_features[3][0]),
            'Acousticness': float(optimal_features[4][0]),
            'Liveness': float(optimal_features[5][0]),
            'Valence': float(optimal_features[6][0]),
            'Tempo': float(optimal_features[7][0]),
            'Duration': int(optimal_features[8][0]),
            'Time_signature': int(optimal_features[9][0])
        }
        search = self.recommendations(limit=limit,
                                      seed_tracks=self.get_recent_id(),
                                      target_danceability=features['Danceability'],
                                      target_energy=features['Energy'],
                                      target_mode=features['Mode'],
                                      target_speechiness=features['Speechiness'],
                                      target_acousticness=features['Acousticness'],
                                      target_liveness=features['Liveness'],
                                      target_valence=features['Valence'],
                                      target_tempo=features['Tempo'],
                                      target_time_signature=4)
        if search:
            answers = []
            for i in search['tracks']:
                _ = []
                track_name = i['name']
                track_id = i['id']
                artist_name = i['artists'][0]['name']
                artist_id = i['artists'][0]['id']
                _.append(track_id)
                _.append(track_name)
                _.append(artist_id)
                _.append(artist_name)
                answers.append(_)
            return answers
        else:
            return 'no suggestions found'


# For testing Class functionality
optimal = [[1.00345916e-01],
           [1.11695381e-01],
           [9.34469830e-02],
           [1.05126139e-01],
           [9.52455139e-02],
           [9.30148881e-02],
           [1.04208585e+05],
           [8.84359745e+01],
           [1.19983206e+05],
           [8.84974123e-02]]

"""calls = APICalls(username) # '31lim2ii6s23jjdsdmdcjgdxpyey'
optimal1 = calls.get_song_features('Want U back')
print(calls.search_by_features(optimal))
print(calls.recently_played_song_features())"""
