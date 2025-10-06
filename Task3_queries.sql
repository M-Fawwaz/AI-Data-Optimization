use eklipse;

# Active Streamers
SELECT COUNT(DISTINCT gs.user_id) AS active_streamers
FROM game_session gs
JOIN clips c ON gs.id = c.gamesession_Id;

# Top 10 User Productive
SELECT gs.user_id,
       COUNT(c.id) AS total_clips
FROM game_session as gs
JOIN clips c ON gs.id = c.gamesession_Id
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10;

# Clip Engagement
SELECT 
    c.id AS clip_id,
    COUNT(DISTINCT d.id) AS downloads,
    COUNT(s.clip_id) AS shares
FROM clips c
LEFT JOIN downloaded_clips d ON c.id = d.clip_id
LEFT JOIN shared_clips s ON c.id = s.clip_id
GROUP BY c.id
ORDER BY 2 DESC, 3 DESC
LIMIT 10;

# Top Games
SELECT gs.game_name,
       COUNT(c.id) AS total_clips,
       SUM (gs.duration) AS total_duration
FROM game_session gs
JOIN clips c ON gs.id = c.gamesession_id
GROUP BY gs.game_name
ORDER BY total_clips DESC
LIMIT 10;

# Premium User VS Free User
SELECT 
    CASE WHEN p.user_id IS NOT NULL THEN 'Premium' ELSE 'Free' END AS user_type,
    AVG(clip_count) AS avg_clips_per_user
FROM (
    SELECT gs.user_id, COUNT(c.id) AS clip_count
    FROM game_session gs
    JOIN clips c ON gs.id = c.gamesession_id
    GROUP BY gs.user_id
) sub
LEFT JOIN premium p ON sub.user_id = p.user_id
GROUP BY user_type;