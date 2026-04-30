"""
Base Crawler
모든 크롤러의 부모 클래스
"""
from abc import ABC, abstractmethod
from src.connectors.db_connector import get_db_connection
from src.utils.discord_helper import send_crawling_success, send_crawling_error


class BaseCrawler(ABC):
    """크롤러 베이스 클래스"""
    
    def __init__(self, crawler_name: str):
        """
        Args:
            crawler_name: 크롤러 이름
        """
        self.crawler_name = crawler_name
        self.db_conn = None
        self.db_cursor = None
    
    def connect_db(self):
        """데이터베이스 연결"""
        try:
            self.db_conn = get_db_connection()
            self.db_cursor = self.db_conn.cursor()
            print(f"✅ [{self.crawler_name}] DB 연결 성공")
        except Exception as e:
            print(f"❌ [{self.crawler_name}] DB 연결 실패: {e}")
            raise
    
    def close_db(self):
        """데이터베이스 연결 종료"""
        if self.db_cursor:
            self.db_cursor.close()
        if self.db_conn:
            self.db_conn.close()
        print(f"✅ [{self.crawler_name}] DB 연결 종료")
    
    @abstractmethod
    def crawl(self, artist: dict):
        """
        크롤링 실행 (하위 클래스에서 구현 필요)
        
        Args:
            artist: 아티스트 정보 딕셔너리
        
        Returns:
            dict: 크롤링 데이터
        """
        pass
    
    @abstractmethod
    def save_to_db(self, data: dict):
        """
        데이터베이스에 저장 (하위 클래스에서 구현 필요)
        
        Args:
            data: 저장할 데이터
        """
        pass
    
    def run(self, artist: dict):
        """
        크롤링 전체 프로세스 실행
        
        Args:
            artist: 아티스트 정보 딕셔너리
        """
        try:
            print(f"🚀 [{self.crawler_name}] 크롤링 시작: {artist['name']}")
            
            # DB 연결
            self.connect_db()
            
            # 크롤링 실행
            data = self.crawl(artist)
            
            if data:
                # DB 저장
                self.save_to_db(data)
                print(f"✅ [{self.crawler_name}] 크롤링 완료")
                
                # Discord 알림
                send_crawling_success(self.crawler_name, 1)
            else:
                print(f"⚠️  [{self.crawler_name}] 크롤링 데이터 없음")
            
        except Exception as e:
            error_msg = str(e)
            print(f"❌ [{self.crawler_name}] 크롤링 실패: {error_msg}")
            
            # Discord 알림
            send_crawling_error(self.crawler_name, error_msg)
            
            raise
        
        finally:
            # DB 연결 종료
            self.close_db()
