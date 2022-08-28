import psycopg2
import requests
import json

connection = psycopg2.connect(
                                database = "airflow",
                                user = "airflow",
                                password = "airflow",
                                host = "database",
                                port = '5432'
                            )


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
    print(channelId, '\n', channelTitle)

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
        videoId.append(video_id)
    return channelId, channelTitle, videoId


if __name__ == '__main__':
    video_data = ['vSmR5kOKPdY']
    token = get_api()
    # for video in video_data:
    #     channelId, channelTitle, videoId = get_information(video, token)
    #     cur = connection.cursor()
    #     # insert channel information
    #     query = f'''INSERT INTO "channel"(channel_id, channel_title) VALUES('{channelId}', '{channelTitle}')'''
    #     cur.execute(query)
    #     cur.close()
    cur = connection.cursor()
    query = f'''INSERT INTO "channel"(channel_id, channel_title) VALUES('a', 'b');'''
    cur.close()