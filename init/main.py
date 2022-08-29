import psycopg2
import requests
import json


def get_api():
    with open('./credentials/youtube_api.json', 'r') as fp:
        token = json.load(fp)['token']
        return token

def get_information(video: str, api_key: str):
    url_video = f'https://www.googleapis.com/youtube/v3/videos?id={video}&key={api_key}&part=snippet'
    response_video = requests.get(url_video)
    response_video = response_video.json()
    
    channelId = (response_video['items'][0]).get('snippet').get('channelId')
    channelTitle = (response_video['items'][0]).get('snippet').get('channelTitle')
    print(channelId, ' ', channelTitle)

    url_channel = f'https://www.googleapis.com/youtube/v3/channels?part=contentDetails&id={channelId}&key={api_key}'
    response_channel = requests.get(url_channel)
    response_channel = response_channel.json()
    

    playListId = response_channel['items'][0].get('contentDetails').get('relatedPlaylists').get('uploads')

    url_playlist = f'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails,status&playlistId={playListId}&key={api_key}&maxResults=20'
    response_playlist = requests.get(url_playlist)
    response_playlist = response_playlist.json()

    videoId = []
    for info in response_playlist['items']:
        video_id = info['contentDetails'].get('videoId')
        videoId.append((channelId, video_id))
    return channelId, channelTitle, videoId

def insert_channel(channelId, channelTitle):
    connection = psycopg2.connect(
                                database = "airflow",
                                user = "airflow",
                                password = "airflow",
                                host = "database",
                                port = '5432'
                            )
    cursor = connection.cursor()
    query = f'''INSERT INTO "channel"(channel_id, channel_title) VALUES('{channelId}', '{channelTitle}')'''
    cursor.execute(query)
    connection.commit()
    cursor.close()

def insert_video(data):
    connection = psycopg2.connect(
                                database = "airflow",
                                user = "airflow",
                                password = "airflow",
                                host = "database",
                                port = '5432'
                            )
    cursor = connection.cursor()
    query = f'''INSERT INTO video(channel_id, video_id) VALUES(%s, %s)'''
    cursor.executemany(query, data)
    connection.commit()
    cursor.close()
  
if __name__ == '__main__':
    data = ['AOIzIh6-q9A&t=547s', 'XV2H9CuQUm8', 'uLnmTXxpK0Q'] # 可以塞你想要的頻道
    token = get_api()
    for video in data:
        channelId, channelTitle, videoId = get_information(video, token)
        try:
            insert_channel(channelId, channelTitle)
            print(f"{channelTitle} insert complete!")
        except:
            print(f"{channelTitle} already in db!")
        try:
            insert_video(videoId)
            print(f"{channelTitle} video insert complete!")
        except:
            print(f"{channelTitle} video already in db!")