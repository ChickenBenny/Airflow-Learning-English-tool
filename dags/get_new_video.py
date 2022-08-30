from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator
import requests
import json
import psycopg2
from datetime import datetime, timedelta
from airflow import DAG

default_args = {
    'owner': 'Benny Hsiao',
    'start_date': datetime(2022, 8, 29, 10, 0),
    'schedule_interval': '@weekly',
    'retries': 2,
    'retry_delay': timedelta(minutes = 5)
}

POSTGRES_CONN_ID = 'database'

def get_api():
    with open('/opt/airflow/dags/credentials/youtube_api.json', 'r') as fp:
        token = json.load(fp)['token']
        return token

def get_channel_info():
    hook = PostgresHook.get_hook(POSTGRES_CONN_ID)
    conn = hook.get_conn()
    cursor = conn.cursor()
    query = '''SELECT channel_id, playlist_id FROM channel;''' 
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    return rows

def check_video_is_exit(video_id):
    hook = PostgresHook.get_hook(POSTGRES_CONN_ID)
    conn = hook.get_conn()
    cursor = conn.cursor()
    query = f'''SELECT video_id FROM video WHERE video_id = '{video_id}';''' 
    cursor.execute(query)
    if cursor.fetchall():
        return True
    else:
        return False


def get_update_info(ti):
    data = ti.xcom_pull(task_ids='get_channel_info', key='return_value')
    token = get_api()
    video_do_not_store = []
    for info in data:
        channel_id = info[0]
        playlist_id = info[1]
        url_playlist = f'https://www.googleapis.com/youtube/v3/playlistItems?part=snippet,contentDetails,status&playlistId={playlist_id}&key={token}&maxResults=3'
        response_playlist = requests.get(url_playlist)
        response_playlist = response_playlist.json()
        for info in response_playlist['items']:
            video_id = info['contentDetails'].get('videoId')
            if check_video_is_exit(video_id):
                continue
            else:
                video_do_not_store.append((channel_id, video_id))
    if len(video_do_not_store) == 0:
        return 'do_nothing'
    else:
        return video_do_not_store

def insert_db_or_not(ti):
    flag = ti.xcom_pull(task_ids = 'get_update_info_task', key = 'return_value')
    if flag == 'do_nothing':
        return 'do_nothing'
    else:
        return 'insert_db'

def insert_db(ti):
    datas = ti.xcom_pull(task_ids = 'get_update_info', key = 'return_value')
    for data in datas:
        connection = psycopg2.connect(
                                database = "airflow",
                                user = "airflow",
                                password = "airflow",
                                host = "database",
                                port = '5432'
                            )
        cursor = connection.cursor()
        query = f'''INSERT INTO video(channel_id, video_id) VALUES(%s, %s)'''
        cursor.execute(query, data)
        connection.commit()
        cursor.close()


with DAG(
    dag_id = 'get_new_video',
    default_args = default_args,
    description = 'weekly get the video information'
) as dag:
    get_channel_info_task = PythonOperator(
        task_id = 'get_channel_info',
        python_callable = get_channel_info,
    )

    get_update_info_task = PythonOperator(
        task_id = 'get_update_info',
        python_callable = get_update_info,
    )

    insert_db_or_not_task = BranchPythonOperator(
        task_id = 'insert_db_or_not',
        python_callable = insert_db_or_not
    )

    insert_db_task = PythonOperator(
        task_id = 'insert_db',
        python_callable = insert_db
    )

    do_nothing_task = DummyOperator(task_id = 'do_nothing')

    get_channel_info_task >> get_update_info_task >> insert_db_or_not_task
    insert_db_or_not_task >> [insert_db_task, do_nothing_task]