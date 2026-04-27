"""
Database Connector
MySQL 데이터베이스 연결 관리
"""
import os
import pymysql
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()


def get_db_connection():
    """
    MySQL 데이터베이스 연결 객체를 반환합니다.
    
    환경변수:
        DB_HOST: MySQL 호스트 (기본값: 127.0.0.1)
        DB_PORT: MySQL 포트 (기본값: 3306)
        DB_USERNAME: MySQL 사용자 (루트 .env와 통일)
        DB_PASSWORD: MySQL 비밀번호
        DB_DATABASE: 데이터베이스 이름 (루트 .env와 통일)
    
    Returns:
        pymysql.Connection: MySQL 연결 객체
        
    Raises:
        pymysql.MySQLError: 데이터베이스 연결 실패 시
    """
    try:
        connection = pymysql.connect(
            host=os.getenv('DB_HOST', '127.0.0.1'),
            port=int(os.getenv('DB_PORT', 3306)),
            user=os.getenv('DB_USERNAME', 'root'),  # DB_USER → DB_USERNAME (통일)
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_DATABASE', 'sm_artist_insights'),  # DB_NAME → DB_DATABASE (통일)
            cursorclass=pymysql.cursors.DictCursor,
            charset='utf8mb4'
        )
        print(f"✅ DB 연결 성공: {os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_DATABASE')}")
        return connection
    except pymysql.MySQLError as e:
        print(f"❌ DB Connection Error: {e}")
        raise e


def test_connection():
    """데이터베이스 연결 테스트"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()
        print(f"MySQL Version: {version}")
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Connection test failed: {e}")
        return False


if __name__ == "__main__":
    # 단독 실행 시 연결 테스트
    test_connection()
