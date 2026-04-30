from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys
import os

# Airflow가 src 폴더의 모듈을 인식할 수 있도록 경로 추가
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from crawlers.youtube_crawler import YoutubeCrawler

# DAG 기본 설정 (재시도 횟수, 시작일 등)
default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'start_date': datetime(2026, 4, 16),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def run_youtube_crawler():
    """아티스트 목록을 순회하며 유튜브 데이터를 수집하는 태스크"""
    # 실제 운영 시에는 db_connector를 이용해 DB에서 아티스트 목록을(SELECT * FROM artists) 조회해와야 합니다.
    target_artists = [
        {"id": 1, "name": "aespa"},
        {"id": 2, "name": "NCT 127"}
    ]
    
    crawler = YoutubeCrawler()
    for artist in target_artists:
        crawler.execute(artist)

# DAG 정의 (매일 자정에 실행)
with DAG(
    'youtube_data_collection_dag',
    default_args=default_args,
    description='유튜브 글로벌 지표 및 댓글 데이터 자동 수집',
    schedule_interval='0 0 * * *', # Cron 표현식: 매일 자정
    catchup=False,
    tags=['sm', 'youtube', 'pipeline'],
) as dag:

    collect_youtube_task = PythonOperator(
        task_id='collect_youtube_task',
        python_callable=run_youtube_crawler,
    )

    # 태스크가 여러 개라면 여기에 의존성(>> 연산자)을 설정합니다.
    collect_youtube_task