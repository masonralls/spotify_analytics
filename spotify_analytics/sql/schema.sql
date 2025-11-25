CREATE TABLE artists (
    artist_id VARCHAR PRIMARY KEY,
    name TEXT NOT NULL,
    genres TEXT,
    popularity INTEGER,
    followers BIGINT
);
CREATE TABLE albums (
    album_id VARCHAR PRIMARY KEY,
    name TEXT NOT NULL,
    release_date DATE,
    total_tracks INTEGER
);
CREATE TABLE tracks (
    track_id VARCHAR PRIMARY KEY,
    name TEXT NOT NULL,
    album_id VARCHAR REFERENCES albums(album_id),
    duration_ms INTEGER,
    explicit BOOLEAN,
    popularity INTEGER
);
CREATE TABLE track_artists (
    track_id VARCHAR REFERENCES tracks(track_id),
    artist_id VARCHAR REFERENCES artists(artist_id),
    PRIMARY KEY (track_id, artist_id)
);
CREATE TABLE audio_features (
    track_id VARCHAR PRIMARY KEY REFERENCES tracks(track_id),
    danceability NUMERIC,
    energy NUMERIC,
    valence NUMERIC,
    tempo NUMERIC,
    acousticness NUMERIC,
    instrumentalness NUMERIC,
    liveness NUMERIC,
    speechiness NUMERIC
);
CREATE TABLE listening_history (
    play_id BIGSERIAL PRIMARY KEY,
    played_at TIMESTAMPTZ NOT NULL,
    track_id VARCHAR REFERENCES tracks(track_id),
    context TEXT,
    source TEXT
);



