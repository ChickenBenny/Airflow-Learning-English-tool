from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.telegram.operators.telegram import TelegramOperator
from datetime import datetime, timedelta
from airflow import DAG
import json

default_args = {
    'owner': 'Benny Hsiao',
    'start_date': datetime(2022, 8, 29, 0, 0),
    'schedule_interval': '@daily',
    'retries': 2,
    'retry_delay': timedelta(minutes = 5)
}

def get_id():
    with open('/opt/airflow/dags/credentials/telegram_api.json', 'r') as fp:
        id = json.load(fp)['id']
        return id    

POSTGRES_CONN_ID = 'database'
TELEGRAM_CONN_ID = 'telegram'
CHAT_ID = get_id()

def get_video_id():
    hook = PostgresHook.get_hook(POSTGRES_CONN_ID)
    conn = hook.get_conn()
    cursor = conn.cursor()
    query = '''SELECT video_id FROM video WHERE video_id NOT IN (SELECT video_id FROM history)ORDER BY RANDOM() LIMIT 1;'''    
    cursor.execute(query)
    rows = cursor.fetchall()
    cursor.close()
    if len(rows) == 1:
        return (rows[0])[0]
    else:
        return "none"

def have_video_or_not(ti):
    flag = ti.xcom_pull(task_ids = 'get_video_id', key = 'return_value')
    if flag == 'none':
        return 'do_nothing'
    else:
        return 'send_task'


with DAG(
    dag_id = 'generate_video',
    default_args = default_args,
    description = 'daily generate the video'
) as dag:
    get_video_id_task = PythonOperator(
        task_id = 'get_video_id',
        python_callable = get_video_id
    )

    have_video_or_not_task = BranchPythonOperator(
        task_id = 'have_video_or_not',
        python_callable = have_video_or_not
    )

    send_video_task = TelegramOperator(
        task_id = 'send_task',
        telegram_conn_id = TELEGRAM_CONN_ID,
        chat_id = CHAT_ID,
        text = "https://www.youtube.com/watch?v={{ ti.xcom_pull(task_ids='get_video_id', key='return_value') }}"        
    )

    insert_history_task =  PostgresOperator(
        task_id = 'insert_history',
        postgres_conn_id  = POSTGRES_CONN_ID,
        sql = '''
                INSERT INTO history(dt, video_id) VALUES('{{ ds  }}', '{{ ti.xcom_pull(task_ids='get_video_id', key='return_value') }}');
        '''
    )


    do_nothing_task = DummyOperator(task_id = 'do_nothing')

    get_video_id_task >> have_video_or_not_task >> [do_nothing_task, send_video_task]
    send_video_task >> insert_history_task 