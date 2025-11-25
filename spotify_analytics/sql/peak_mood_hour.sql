SELECT
    EXTRACT(HOUR FROM played_at) AS hour,
    AVG(valence) AS avg_valence
FROM listening_history lh
JOIN audio_features af ON lh.track_id = af.track_id
GROUP BY hour
ORDER BY hour;
