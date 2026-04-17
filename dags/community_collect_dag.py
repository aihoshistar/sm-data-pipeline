from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.crawlers.community_crawler import CommunityCrawler

default_args = {
    'owner': 'data_engineer',
    'depends_on_past': False,
    'start_date': datetime(2026, 4, 16),
    'retries': 1,
    'retry_delay': timedelta(minutes=10),
}

def run_community_crawler():
    """아티스트 목록을 순회하며 국내 커뮤니티 게시글 수집"""
    target_artists = [
        {"id": 1, "name": "aespa"},
        {"id": 2, "name": "NCT 127"}
    ]
    
    crawler = CommunityCrawler()
    for artist in target_artists:
        crawler.execute(artist)

# DAG 정의 (오전 8시, 오후 8시 실행)
with DAG(
    'community_collection_dag',
    default_args=default_args,
    description='국내 커뮤니티(더쿠, 인스티즈 등) 여론 데이터 수집',
    schedule_interval='0 8,20 * * *', # Cron 표현식: 매일 08시, 20시
    catchup=False,
    tags=['sm', 'community', 'sentiment', 'pipeline'],
) as dag:

    collect_community_task = PythonOperator(
        task_id='collect_community_task',
        python_callable=run_community_crawler,
    )

    collect_community_task