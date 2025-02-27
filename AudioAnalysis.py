import os
import uuid
import librosa
import numpy as np
import subprocess
import concurrent.futures
import json

CACHE_FILE = "audio_features_cache.json"

class AudioAnalysis:
    def __init__(self):
        """
        Initialize the extractor.
        """
        self.features = ['Artist Name', 'Track Name', 'Danceability', 'Energy',
                         'Loudness', 'Mode', 'Speechiness', 'Acousticness', 'Liveness',
                         'Valence', 'Tempo', 'Duration', 'Time Signature']
        self.cache = self._load_cache()

    def _load_cache(self):
        """Load cached features from JSON file."""
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        return {}

    def _save_cache(self):
        """Save extracted features to cache file."""
        with open(CACHE_FILE, "w") as f:
            json.dump(self.cache, f, indent=4, default=lambda x: float(x) if isinstance(x, np.float32) else x)

    def _download_audio(self, song_name, artist_name):
        """
        Download the song from YouTube as an audio file.
        Returns the filename or None if failed.
        """
        search_query = f"{song_name} {artist_name} offical audio"
        output_filename = f"temp_audio_{uuid.uuid4().hex}.mp3"

        cmd = [
            "yt-dlp", "--quiet", "--no-warnings", "--extract-audio", "--audio-format", "mp3",
            "--output", output_filename, "--limit-rate", "500K", f"ytsearch:{search_query}"
        ]

        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        if result.returncode != 0:
            return None

        return output_filename

    def _extract_features(self, file_path):
        """
        Extract audio features from the downloaded file using Librosa.
        Uses only the first 30 seconds for faster processing.
        """
        full_duration = librosa.get_duration(filename=file_path)
        y, sr = librosa.load(file_path, sr=22050, duration=30)
        features = {}

        # Tempo & Beat Tracking
        onset_env = librosa.onset.onset_strength(y=y, sr=sr)
        tempo, beats = librosa.beat.beat_track(y=y, sr=sr, onset_envelope=onset_env)

        # Danceability (beat consistency)
        beat_diff = np.diff(beats) if len(beats) > 1 else [1]
        features["Danceability"] = float(np.std(beat_diff).item()) / float((np.mean(beat_diff) + 1e-6))

        # Energy
        rms = librosa.feature.rms(y=y)
        features["Energy"] = (np.mean(rms).item())

        # Mode (Major = 1, Minor = 0)
        chroma = librosa.feature.chroma_stft(y=y, sr=sr)
        mode = np.argmax(np.mean(chroma, axis=1))
        features["Mode"] = 1 if mode in [0, 4, 7] else 0

        # Speechiness (using zero-crossing rate)
        zcr = librosa.feature.zero_crossing_rate(y)
        features["Speechiness"] = float(np.mean(zcr).item())

        # Acousticness (inverse of spectral centroid)
        spec_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
        features["Acousticness"] = 1 - float(np.mean(spec_centroid) / np.max(spec_centroid))

        # Liveness (spikes in amplitude)
        features["Liveness"] = float(np.mean(np.abs(np.diff(y))).item())

        # Valence (harmonic contrast)
        contrast = librosa.feature.spectral_contrast(y=y, sr=sr)
        features["Valence"] = float(np.exp(-np.mean(contrast)))

        features["Tempo"] = float(tempo.item())

        # Duration
        features["Duration"] = float(full_duration) * 1000

        features["Time Signature"] = 4

        # Normalize Features (like Spotify)
        for key in ["Danceability", "Energy", "Speechiness", "Acousticness", "Liveness"]:
            features[key] = round(features[key] / max(features[key], 1), 4)

        return features

    def _cleanup(self, file_path):
        """Delete the downloaded file after processing."""
        if os.path.exists(file_path):
            os.remove(file_path)

    def _process_single_song(self, song_name, artist_name):
        """Process a single song and return its features."""
        key = f"{artist_name} - {song_name}"

        if key in self.cache:
            return [artist_name, song_name] + [self.cache[key]]

        file_path = self._download_audio(song_name, artist_name)
        if not file_path:
            return [artist_name, song_name] + ["N/A"] * (len(self.features) - 2)

        features = self._extract_features(file_path)
        self._cleanup(file_path)

        self.cache[key] = features  # Save to cache
        self._save_cache()

        return [artist_name, song_name] + [features]

    def process_songs_parallel(self, song_list, max_workers=10):
        """
        Process multiple songs in parallel using threading.
        max_workers: Number of songs to download/analyze at the same time.
        """
        results = []

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            results += list(executor.map(lambda song: self._process_single_song(*song), song_list))

        return results

"""songs = [
    ["Blinding Lights", "The Weeknd"],
    ["Shape of You", "Ed Sheeran"],
    ["Uptown Funk", "Bruno Mars"],
    ["Someone Like You", "Adele"]
]

extractor = AudioFeatureExtractor()
results = extractor.process_songs_parallel(songs, max_workers=5)  # Adjust workers based on your CPU

for row in results:
    print(row)"""

