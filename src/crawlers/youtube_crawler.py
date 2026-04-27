"""
YouTube Crawler
YouTube 영상 통계 크롤링
"""
from crawlers.base_crawler import BaseCrawler
from datetime import datetime


class YoutubeCrawler(BaseCrawler):
    """YouTube 영상 통계 크롤러"""
    
    def __init__(self):
        super().__init__(platform_name="YouTube")

    def crawl(self, artist_info: dict) -> dict:
        """
        YouTube 영상 통계 크롤링
        
        TODO: YouTube Data API v3 또는 Selenium을 사용한 실제 크롤링 구현
        
        Args:
            artist_info: 아티스트 정보
        
        Returns:
            YouTube 통계 데이터
        """
        # 현재는 임시 더미 데이터 반환
        # 실제 구현 시 YouTube Data API 또는 크롤링 로직으로 대체
        
        return {
            "artist_id": artist_info['id'],
            "video_id": "dummy_video_123",
            "title": f"{artist_info['name']} - 신곡 MV",  # video_title → title (스키마 일치)
            "view_count": 5000000,
            "like_count": 250000,
            "comment_count": 15000,
            "published_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 추가
        }

    def save_to_db(self, data: dict):
        """
        YouTube 통계를 sns_youtube_stats 테이블에 저장
        
        Args:
            data: YouTube 통계 데이터
        """
        cursor = self.db_conn.cursor()
        
        # 테이블 스키마와 일치하도록 수정
        sql = """
            INSERT INTO sns_youtube_stats 
            (artist_id, video_id, title, view_count, like_count, comment_count, published_at, collected_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
        """
        
        cursor.execute(sql, (
            data['artist_id'],
            data['video_id'],
            data['title'],  # video_title → title
            data['view_count'],
            data['like_count'],
            data['comment_count'],
            data['published_at']  # 추가
        ))
        
        self.db_conn.commit()
        cursor.close()
        
        print(f"✅ YouTube 데이터 저장: video_id={data['video_id']}, views={data['view_count']:,}")


# 테스트용
if __name__ == "__main__":
    crawler = YoutubeCrawler()
    
    # 테스트 아티스트 정보
    test_artist = {
        'id': 1,
        'name': 'aespa'
    }
    
    # 크롤링 실행
    crawler.execute(test_artist)
