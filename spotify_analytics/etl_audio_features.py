from spotify_client import get_spotify_client
from db import engine
from sqlalchemy import text
from spotipy.exceptions import SpotifyException
import time

def fetch_and_store_audio_features(batch_size=50):
    sp = get_spotify_client()

    with engine.begin() as conn:
        # Get tracks that don't have audio features yet
        result = conn.execute(text("""
            SELECT t.track_id
            FROM tracks t
            LEFT JOIN audio_features a ON t.track_id = a.track_id
            WHERE a.track_id IS NULL
        """))
        track_ids = [row[0] for row in result.fetchall()]

        print(f"Found {len(track_ids)} tracks missing audio features")

        for i in range(0, len(track_ids), batch_size):
            batch = track_ids[i:i + batch_size]
            print(f"Fetching features for tracks {i}–{i + len(batch) - 1}")

            try:
                features = sp.audio_features(batch)
            except SpotifyException as e:
                # Log and skip this batch
                print(f"⚠️ Spotify error for batch {i}–{i + len(batch) - 1}: {e}")
                continue

            # Insert only valid feature objects
            for f in features:
                if f is None:
                    continue

                conn.execute(text("""
                    INSERT INTO audio_features (
                        track_id,
                        danceability,
                        energy,
                        valence,
                        tempo,
                        acousticness,
                        instrumentalness,
                        liveness,
                        loudness,
                        speechiness
                    )
                    VALUES (
                        :track_id,
                        :danceability,
                        :energy,
                        :valence,
                        :tempo,
                        :acousticness,
                        :instrumentalness,
                        :liveness,
                        :loudness,
                        :speechiness
                    )
                    ON CONFLICT (track_id) DO UPDATE
                    SET
                        danceability = EXCLUDED.danceability,
                        energy = EXCLUDED.energy,
                        valence = EXCLUDED.valence,
                        tempo = EXCLUDED.tempo,
                        acousticness = EXCLUDED.acousticness,
                        instrumentalness = EXCLUDED.instrumentalness,
                        liveness = EXCLUDED.liveness,
                        loudness = EXCLUDED.loudness,
                        speechiness = EXCLUDED.speechiness
                """), {
                    "track_id": f["id"],
                    "danceability": f["danceability"],
                    "energy": f["energy"],
                    "valence": f["valence"],
                    "tempo": f["tempo"],
                    "acousticness": f["acousticness"],
                    "instrumentalness": f["instrumentalness"],
                    "liveness": f["liveness"],
                    "loudness": f["loudness"],
                    "speechiness": f["speechiness"]
                })

            # Be nice to the API
            time.sleep(0.1)

if __name__ == "__main__":
    fetch_and_store_audio_features()
