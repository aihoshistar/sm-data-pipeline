from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys
import os

# Airflow가 src 폴더의 모듈을 인식할 수 있도록 경로 추가
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.crawlers.x_crawler import XCrawler

default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'start_date': datetime(2026, 4, 16),
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

def run_x_crawler():
    """아티스트 목록을 순회하며 X(Twitter) 실시간 트렌드 및 해시태그 수집"""
    target_artists = [
        {"id": 1, "name": "aespa"},
        {"id": 2, "name": "NCT 127"}
    ]
    
    crawler = XCrawler()
    for artist in target_artists:
        crawler.execute(artist)

# DAG 정의 (6시간마다 실행)
with DAG(
    'x_trend_collection_dag',
    default_args=default_args,
    description='X(Twitter) 실시간 트렌드 및 해시태그 수집 파이프라인',
    schedule_interval='0 */6 * * *', # Cron 표현식: 6시간 간격 (00, 06, 12, 18시)
    catchup=False,
    tags=['sm', 'x', 'twitter', 'pipeline'],
) as dag:

    collect_x_task = PythonOperator(
        task_id='collect_x_trend_task',
        python_callable=run_x_crawler,
    )

    collect_x_task