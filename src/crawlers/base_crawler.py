import abc
from src.connectors.db_connector import get_db_connection
from src.utils.discord_helper import send_discord_alert

class BaseCrawler(abc.ABC):
    def __init__(self, platform_name: str):
        self.platform_name = platform_name
        self.db_conn = get_db_connection()

    @abc.abstractmethod
    def crawl(self, artist_info: dict) -> dict:
        """TODO: 크롤링 기능"""
        pass

    @abc.abstractmethod
    def save_to_db(self, data: dict):
        """TODO: DB 저장"""
        pass

    def execute(self, artist_info: dict):
        """Airflow DAG에서 직접 호출할 함수"""
        try:
            print(f"[{self.platform_name}] {artist_info['name']} 데이터 수집 시작...")
            
            # 1. 크롤링 수행
            data = self.crawl(artist_info)
            
            # 2. DB 저장
            if data:
                self.save_to_db(data)
                print(f"[{self.platform_name}] 데이터 저장 완료.")
            else:
                print(f"[{self.platform_name}] 수집된 데이터가 없습니다.")
                
            return True

        except Exception as e:
            error_msg = f"[{self.platform_name}] 데이터 수집 실패 (Artist: {artist_info.get('name')}): {str(e)}"
            send_discord_alert(error_msg, level="ERROR")
            raise e
        finally:
            if self.db_conn and self.db_conn.open:
                self.db_conn.close()