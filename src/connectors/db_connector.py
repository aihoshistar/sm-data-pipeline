import os
import pymysql
from dotenv import load_dotenv
from connectors.db_connector import get_db_connection


# .env 파일 로드
load_dotenv()

def get_db_connection():
    """MySQL 데이터베이스 연결 객체를 반환합니다."""
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            cursorclass=pymysql.cursors.DictCursor
        )
        return connection
    except pymysql.MySQLError as e:
        print(f"DB Connection Error: {e}")
        raise e

def collect_youtube_task():
    conn = get_db_connection()
    