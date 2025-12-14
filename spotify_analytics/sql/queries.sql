-- sanity check --
SELECT 'listening_history' AS table_name, COUNT(*) FROM listening_history
UNION ALL
SELECT 'tracks',            COUNT(*) FROM tracks
UNION ALL
SELECT 'artists',           COUNT(*) FROM artists
UNION ALL
SELECT 'albums',            COUNT(*) FROM albums
UNION ALL
SELECT 'track_artists',     COUNT(*) FROM track_artists;

-- top artists --
SELECT ar.artist_id,
       ar.name,
       COUNT(*) AS plays
FROM listening_history lh
JOIN track_artists ta ON lh.track_id = ta.track_id
JOIN artists ar       ON ta.artist_id = ar.artist_id
GROUP BY ar.artist_id, ar.name
ORDER BY plays DESC
LIMIT 20;

-- top tracks --
SELECT t.track_id,
       t.name,
       COUNT(*) AS plays
FROM listening_history lh
JOIN tracks t ON lh.track_id = t.track_id
GROUP BY t.track_id, t.name
ORDER BY plays DESC
LIMIT 20;

-- top albums --
SELECT al.album_id,
       al.name,
       COUNT(*) AS plays
FROM listening_history lh
JOIN tracks t  ON lh.track_id = t.track_id
JOIN albums al ON t.album_id = al.album_id
GROUP BY al.album_id, al.name
ORDER BY plays DESC
LIMIT 20;

-- plays by hour of day --
SELECT EXTRACT(HOUR FROM played_at) AS hour_of_day,
       COUNT(*) AS plays
FROM listening_history
GROUP BY hour_of_day
ORDER BY hour_of_day;

-- plays by day of week (stable ordering) --
SELECT EXTRACT(ISODOW FROM played_at) AS dow_num,
       TO_CHAR(played_at, 'Dy')       AS dow,
       COUNT(*)                       AS plays
FROM listening_history
GROUP BY dow_num, dow
ORDER BY dow_num;

-- first time each artist was played --
CREATE MATERIALIZED VIEW IF NOT EXISTS artist_first_play AS
SELECT ta.artist_id,
       MIN(lh.played_at) AS first_played_at
FROM listening_history lh
JOIN track_artists ta ON lh.track_id = ta.track_id
GROUP BY ta.artist_id;

-- new artists discovered per day --
SELECT DATE(first_played_at) AS discovery_date,
       COUNT(*)              AS new_artists
FROM artist_first_play
GROUP BY discovery_date
ORDER BY discovery_date;

-- full listening history with track names --
SELECT
    lh.played_at,
    lh.track_id,
    t.name AS track_name,
    STRING_AGG(ar.name, ', ' ORDER BY ar.name) AS artist_names
FROM listening_history lh
JOIN tracks t          ON lh.track_id = t.track_id
JOIN track_artists ta  ON t.track_id = ta.track_id
JOIN artists ar        ON ta.artist_id = ar.artist_id
GROUP BY
    lh.played_at,
    lh.track_id,
    t.name
ORDER BY lh.played_at;


