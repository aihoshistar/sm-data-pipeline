"""
YouTube Crawler
YouTube 비디오 데이터 수집
"""
from src.crawlers.base_crawler import BaseCrawler
from datetime import datetime


class YoutubeCrawler(BaseCrawler):
    """YouTube 크롤러"""
    
    def __init__(self):
        super().__init__("YouTube Crawler")
    
    def crawl(self, artist: dict):
        """
        YouTube 비디오 크롤링
        
        Args:
            artist: 아티스트 정보 {'id': 1, 'name': 'aespa', ...}
        
        Returns:
            dict: 크롤링 데이터
        """
        print(f"🔍 [{self.crawler_name}] {artist['name']} YouTube 데이터 수집 중...")
        
        # TODO: 실제 YouTube Data API 구현
        # 현재는 더미 데이터 반환
        data = {
            'artist_id': artist['id'],
            'video_id': 'dummy_video_123',
            'title': f"{artist['name']} - Latest Video",
            'description': 'This is a test video',
            'thumbnail_url': 'https://i.ytimg.com/vi/dummy/maxresdefault.jpg',
            'view_count': 1000000,
            'like_count': 50000,
            'comment_count': 5000,
            'published_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return data
    
    def save_to_db(self, data: dict):
        """
        PostgreSQL에 데이터 저장
        
        Args:
            data: 저장할 YouTube 데이터
        """
        sql = """
        INSERT INTO crawled_youtube_videos (
            artist_id, video_id, title, description, thumbnail_url,
            view_count, like_count, comment_count, published_at, created_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        ON CONFLICT (video_id) 
        DO UPDATE SET
            view_count = EXCLUDED.view_count,
            like_count = EXCLUDED.like_count,
            comment_count = EXCLUDED.comment_count,
            updated_at = NOW()
        """
        
        self.db_cursor.execute(sql, (
            data['artist_id'],
            data['video_id'],
            data['title'],
            data['description'],
            data['thumbnail_url'],
            data['view_count'],
            data['like_count'],
            data['comment_count'],
            data['published_at']
        ))
        
        self.db_conn.commit()
        print(f"💾 [{self.crawler_name}] DB 저장 완료: {data['video_id']}")


if __name__ == '__main__':
    # 테스트 실행
    crawler = YoutubeCrawler()
    test_artist = {'id': 1, 'name': 'aespa'}
    crawler.run(test_artist)
