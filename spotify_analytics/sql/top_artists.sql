SELECT ar.name, COUNT(*) AS plays
FROM listening_history lh
JOIN track_artists ta ON lh.track_id = ta.track_id
JOIN artists ar ON ta.artist_id = ar.artist_id
GROUP BY ar.name
ORDER BY plays DESC
LIMIT 10;

--join listening_history with track_artists to get artist IDs for each track listened to
--then join with artists table to get artist names
--group by artist name and count number of plays
--order by play count descending and limit to top 10 artists