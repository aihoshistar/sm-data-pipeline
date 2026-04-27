"""
Base Crawler
모든 크롤러의 베이스 클래스
"""
import abc
from connectors.db_connector import get_db_connection  # src. 제거
from utils.discord_helper import send_discord_alert  # src. 제거


class BaseCrawler(abc.ABC):
    """
    모든 크롤러의 추상 베이스 클래스
    
    Args:
        platform_name: 플랫폼 이름 (예: "YouTube", "X(Twitter)")
    """
    
    def __init__(self, platform_name: str):
        self.platform_name = platform_name
        self.db_conn = get_db_connection()

    @abc.abstractmethod
    def crawl(self, artist_info: dict) -> dict:
        """
        크롤링 수행 (추상 메소드)
        
        Args:
            artist_info: 아티스트 정보 딕셔너리
                - id: 아티스트 ID
                - name: 아티스트 이름
        
        Returns:
            크롤링된 데이터 딕셔너리
        """
        pass

    @abc.abstractmethod
    def save_to_db(self, data: dict):
        """
        DB 저장 (추상 메소드)
        
        Args:
            data: 저장할 데이터 딕셔너리
        """
        pass

    def execute(self, artist_info: dict) -> bool:
        """
        크롤링 실행 및 저장 (Airflow DAG에서 호출)
        
        Args:
            artist_info: 아티스트 정보 딕셔너리
        
        Returns:
            성공 여부 (True/False)
        """
        try:
            print(f"[{self.platform_name}] {artist_info['name']} 데이터 수집 시작...")
            
            # 1. 크롤링 수행
            data = self.crawl(artist_info)
            
            # 2. DB 저장
            if data:
                self.save_to_db(data)
                print(f"[{self.platform_name}] 데이터 저장 완료: {data}")
                
                # 성공 알림 (선택 사항)
                # send_discord_alert(
                #     f"[{self.platform_name}] {artist_info['name']} 데이터 수집 완료",
                #     level="INFO"
                # )
            else:
                print(f"[{self.platform_name}] 수집된 데이터가 없습니다.")
                
            return True

        except Exception as e:
            error_msg = (
                f"[{self.platform_name}] 데이터 수집 실패\n"
                f"Artist: {artist_info.get('name', 'Unknown')}\n"
                f"Error: {str(e)}"
            )
            print(f"❌ {error_msg}")
            send_discord_alert(error_msg, level="ERROR")
            raise e
            
        finally:
            # DB 연결 종료
            if self.db_conn and self.db_conn.open:
                self.db_conn.close()
                print(f"[{self.platform_name}] DB 연결 종료")
