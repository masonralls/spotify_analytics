from spotify_client import get_spotify_client
from db import engine
from sqlalchemy import text
from datetime import datetime

def upsert_track_metadata(conn, track):
    track_id = track["id"]
    name = track["name"]
    popularity = track.get("popularity")

    # Album data
    album = track["album"]
    album_id = album["id"]
    album_name = album["name"]
    release_date = album.get("release_date")
    total_tracks = album.get("total_tracks")

    # --- UPSERT album ---
    conn.execute(text("""
        INSERT INTO albums (album_id, name, release_date, total_tracks)
        VALUES (:album_id, :name, :release_date, :total_tracks)
        ON CONFLICT (album_id) DO UPDATE
        SET name = EXCLUDED.name
    """), {
        "album_id": album_id,
        "name": album_name,
        "release_date": release_date,
        "total_tracks": total_tracks
    })

    # --- UPSERT track ---
    conn.execute(text("""
        INSERT INTO tracks (track_id, name, album_id, duration_ms, explicit, popularity)
        VALUES (:track_id, :name, :album_id, :duration_ms, :explicit, :popularity)
        ON CONFLICT (track_id) DO UPDATE
        SET name = EXCLUDED.name,
            popularity = EXCLUDED.popularity
    """), {
        "track_id": track_id,
        "name": name,
        "album_id": album_id,
        "duration_ms": track.get("duration_ms"),
        "explicit": track.get("explicit"),
        "popularity": popularity
    })

    # --- UPSERT artists + relationship ---
    for artist in track["artists"]:
        artist_id = artist["id"]
        artist_name = artist["name"]

        # Insert artist
        conn.execute(text("""
            INSERT INTO artists (artist_id, name)
            VALUES (:artist_id, :name)
            ON CONFLICT (artist_id) DO UPDATE
            SET name = EXCLUDED.name
        """), {"artist_id": artist_id, "name": artist_name})

        # Insert link table
        conn.execute(text("""
            INSERT INTO track_artists (track_id, artist_id)
            VALUES (:track_id, :artist_id)
            ON CONFLICT DO NOTHING
        """), {"track_id": track_id, "artist_id": artist_id})


def fetch_and_store_recently_played(limit=50):
    sp = get_spotify_client()
    results = sp.current_user_recently_played(limit=limit)

    with engine.begin() as conn:
        for item in results["items"]:
            played_at_raw = item["played_at"]
            played_at = datetime.fromisoformat(played_at_raw.replace("Z", "+00:00"))
            track = item["track"]

            # Metadata
            upsert_track_metadata(conn, track)

            # Listening history
            conn.execute(text("""
                INSERT INTO listening_history (played_at, track_id, source)
                VALUES (:played_at, :track_id, 'recently_played')
                ON CONFLICT DO NOTHING
            """), {
                "played_at": played_at,
                "track_id": track["id"]
            })

if __name__ == "__main__":
    fetch_and_store_recently_played()
