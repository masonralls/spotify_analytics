SELECT ar.name, COUNT(*) AS plays
FROM listening_history lh
JOIN track_artists ta ON lh.track_id = ta.track_id
JOIN artists ar ON ta.artist_id = ar.artist_id
GROUP BY ar.name
ORDER BY plays DESC
LIMIT 10;
