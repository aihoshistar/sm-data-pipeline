"""
YouTube Data Collection DAG
매일 자정 YouTube 데이터 수집
"""
import sys
import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator

# src 경로 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from crawlers.youtube_crawler import YoutubeCrawler


def get_artists():
    """크롤링 대상 아티스트 목록 조회"""
    from connectors.db_connector import get_db_connection
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, name, youtube_channel_id FROM artists WHERE is_active = true")
    artists = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return [
        {'id': artist[0], 'name': artist[1], 'youtube_channel_id': artist[2]}
        for artist in artists
    ]


def crawl_youtube():
    """YouTube 크롤링 실행"""
    artists = get_artists()
    crawler = YoutubeCrawler()
    
    for artist in artists:
        try:
            crawler.run(artist)
        except Exception as e:
            print(f"❌ {artist['name']} 크롤링 실패: {e}")
            continue


# DAG 기본 설정
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG 정의
dag = DAG(
    'youtube_data_collection_dag',
    default_args=default_args,
    description='YouTube 비디오 데이터 수집',
    schedule_interval='0 0 * * *',  # 매일 자정
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['youtube', 'crawling'],
)

# Task 정의
crawl_task = PythonOperator(
    task_id='crawl_youtube_data',
    python_callable=crawl_youtube,
    dag=dag,
)
