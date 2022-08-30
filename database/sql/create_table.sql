-- create a table to store the channelID and channelTitle
CREATE TABLE IF NOT EXISTS "channel" (
    channel_id TEXT NOT NULL PRIMARY KEY,
    playlist_id TEXT NOT NULL,
    channel_title TEXT NOT NULL
); 

 -- create a table to store vide id and channelID
CREATE TABLE IF NOT EXISTS video (
    channel_id TEXT NOT NULL REFERENCEs channel(channel_id),
    video_id TEXT NOT NULL PRIMARY KEY
);  

  -- create a table to store the video which had been watched
CREATE TABLE IF NOT EXISTS history (
    dt DATE NOT NULL, 
    video_id TEXT NOT NULL REFERENCEs video(video_id) 
);
