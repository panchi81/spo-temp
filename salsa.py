import spotipy
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import pandas as pd

# from os import environ, getenv

# from dotenv import load_dotenv
from dotenv import dotenv_values

# load_dotenv()

config = dotenv_values(".env")

# CLIENT_ID = environ.get("client_id")
# CLIENT_SECRET = environ.get("client_secret")
# USERNAME = environ.get("username")
# SRC_PLAYLIST_ID = environ.get("source_playlist_id")
# DST_PLAYLIST_ID = environ.get("destination_playlist_id")

CLIENT_ID = config["client_id"]
CLIENT_SECRET = config["client_secret"]
USERNAME = config["username"]
SRC_PLAYLIST_ID = config["source_playlist_id"]
DST_PLAYLIST_ID = config["destination_playlist_id"]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        CLIENT_ID,
        CLIENT_SECRET,
        redirect_uri="http://localhost:8888/callback",
        scope="user-library-read",
    )
)


def main():
    track_ids, track_names = get_playlist_tracks(USERNAME, SRC_PLAYLIST_ID)
    playlist_features_df = get_audio_features(track_ids, track_names)
    # playlist_features_df = playlist_features_df[["id", "acousticness", "danceability", "duration_ms",
    #                      "energy", "instrumentalness",  "key", "liveness",
    #                      "loudness", "mode", "speechiness", "tempo", "valence"]]
    playlist_features_df = playlist_features_df[
        ["tempo", "duration_ms", "danceability", "acousticness"]
    ]
    # playlist_features_df.loc['Average'] = playlist_features_df.mean()
    # playlist_features_df.loc[["duration_s"]] = 2
    print(playlist_features_df)


def get_playlist_tracks(USERNAME, SRC_PLAYLIST_ID):
    # no paging
    source_playlist = sp.user_playlist_tracks(USERNAME, SRC_PLAYLIST_ID)
    track_ids = []
    track_names = []
    for track in source_playlist["items"]:
        track_ids.append(track["track"]["id"])
        track_names.append(track["track"]["name"])

    return track_ids, track_names


def get_audio_features(track_ids, track_names):
    features = []
    for id in track_ids:
        audio_features = sp.audio_features(id)
        # Refactor
        # for track in audio_features:
        #     features.append(track)
        # Refactored
        features.extend(iter(audio_features))
    return pd.DataFrame(features, index=track_names)


if __name__ == "__main__":
    main()
