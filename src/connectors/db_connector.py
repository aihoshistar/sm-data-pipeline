"""
Database Connector - PostgreSQL
Airflow 크롤링 데이터 저장용
"""
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_db_connection():
    """
    PostgreSQL 데이터베이스 연결
    
    Returns:
        psycopg2.connection: PostgreSQL 연결 객체
    """
    return psycopg2.connect(
        host=os.getenv('POSTGRES_HOST', 'postgres'),
        port=int(os.getenv('POSTGRES_PORT', 5432)),
        user=os.getenv('POSTGRES_USER', 'postgres'),
        password=os.getenv('POSTGRES_PASSWORD', 'password123'),
        database=os.getenv('POSTGRES_DB', 'sm_crawled_data')
    )


if __name__ == '__main__':
    # 연결 테스트
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ PostgreSQL 연결 성공: {version[0]}")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"❌ PostgreSQL 연결 실패: {e}")
