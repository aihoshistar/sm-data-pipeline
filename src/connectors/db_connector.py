"""
SM AI Backend - Database Connectors
PostgreSQL (읽기) + MySQL (쓰기) 이중 연결
"""
import os
import psycopg2
import pymysql
from dotenv import load_dotenv

load_dotenv()


def get_postgres_connection():
    """
    PostgreSQL 연결 (크롤링 데이터 읽기용)
    Database: sm_crawled_data
    """
    return psycopg2.connect(
        host=os.getenv('POSTGRES_HOST', 'postgres'),
        port=int(os.getenv('POSTGRES_PORT', 5432)),
        user=os.getenv('POSTGRES_USER', 'postgres'),
        password=os.getenv('POSTGRES_PASSWORD', 'password123'),
        database=os.getenv('POSTGRES_DB', 'sm_crawled_data')
    )


def get_mysql_connection():
    """
    MySQL 연결 (AI 분석 결과 저장용)
    Database: sm_artist_insights
    """
    return pymysql.connect(
        host=os.getenv('MYSQL_HOST', 'mysql'),
        port=int(os.getenv('MYSQL_PORT', 3306)),
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', 'password123'),
        database=os.getenv('MYSQL_DB', 'sm_artist_insights'),
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )


# 사용 예시
if __name__ == '__main__':
    # PostgreSQL에서 데이터 읽기
    pg_conn = get_postgres_connection()
    pg_cursor = pg_conn.cursor()
    
    pg_cursor.execute("""
        SELECT * FROM crawled_youtube_videos 
        WHERE artist_id = 1 
        ORDER BY published_at DESC 
        LIMIT 10
    """)
    
    youtube_data = pg_cursor.fetchall()
    print(f"✅ PostgreSQL: {len(youtube_data)} rows")
    
    pg_cursor.close()
    pg_conn.close()
    
    # MySQL에 결과 저장
    mysql_conn = get_mysql_connection()
    mysql_cursor = mysql_conn.cursor()
    
    mysql_cursor.execute("""
        INSERT INTO sns_youtube_stats (
            artist_id, video_count, total_views, total_likes
        ) VALUES (%s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            video_count = VALUES(video_count),
            total_views = VALUES(total_views),
            total_likes = VALUES(total_likes),
            updated_at = NOW()
    """, (1, len(youtube_data), 1000000, 50000))
    
    mysql_conn.commit()
    print("✅ MySQL: 데이터 저장 완료")
    
    mysql_cursor.close()
    mysql_conn.close()
