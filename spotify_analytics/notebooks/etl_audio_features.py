from spotify_client import get_spotify_client
from db import engine
from sqlalchemy import text

def fetch_and_store_audio_features():
    sp = get_spotify_client()

    with engine.begin() as conn:
        # Get all tracks missing audio features
        result = conn.execute(text("""
            SELECT t.track_id
            FROM tracks t
            LEFT JOIN audio_features a ON t.track_id = a.track_id
            WHERE a.track_id IS NULL
        """))

        track_ids = [row[0] for row in result]

        # Spotify API allows 100 track IDs at once
        for i in range(0, len(track_ids), 100):
            batch = track_ids[i:i+100]
            features = sp.audio_features(batch)

            for f in features:
                if f is None:
                    continue

                conn.execute(text("""
                    INSERT INTO audio_features (
                        track_id, danceability, energy, valence, tempo,
                        acousticness, instrumentalness, liveness, speechiness
                    )
                    VALUES (
                        :track_id, :danceability, :energy, :valence, :tempo,
                        :acousticness, :instrumentalness, :liveness, :speechiness
                    )
                    ON CONFLICT (track_id) DO UPDATE
                    SET danceability = EXCLUDED.danceability,
                        energy = EXCLUDED.energy,
                        valence = EXCLUDED.valence,
                        tempo = EXCLUDED.tempo;
                """), {
                    "track_id": f["id"],
                    "danceability": f["danceability"],
                    "energy": f["energy"],
                    "valence": f["valence"],
                    "tempo": f["tempo"],
                    "acousticness": f["acousticness"],
                    "instrumentalness": f["instrumentalness"],
                    "liveness": f["liveness"],
                    "speechiness": f["speechiness"]
                })

if __name__ == "__main__":
    fetch_and_store_audio_features()
