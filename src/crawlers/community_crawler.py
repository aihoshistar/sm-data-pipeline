"""
Community Crawler
더쿠, 인스티즈 등 커뮤니티 게시글 수집
"""
from src.crawlers.base_crawler import BaseCrawler
from datetime import datetime


class CommunityCrawler(BaseCrawler):
    """커뮤니티 크롤러"""
    
    def __init__(self):
        super().__init__("Community Crawler")
    
    def crawl(self, artist: dict):
        """
        커뮤니티 게시글 크롤링
        
        Args:
            artist: 아티스트 정보 {'id': 1, 'name': 'aespa', ...}
        
        Returns:
            dict: 크롤링 데이터
        """
        print(f"🔍 [{self.crawler_name}] {artist['name']} 커뮤니티 데이터 수집 중...")
        
        # TODO: 실제 Selenium 기반 크롤링 구현
        # 현재는 더미 데이터 반환
        data = {
            'artist_id': artist['id'],
            'platform': 'theqoo',
            'post_id': 'dummy_post_123',
            'post_title': f"{artist['name']} 최신 소식",
            'post_url': 'https://theqoo.net/dummy',
            'view_count': 10000,
            'comment_count': 100,
            'posted_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return data
    
    def save_to_db(self, data: dict):
        """
        PostgreSQL에 데이터 저장
        
        Args:
            data: 저장할 커뮤니티 데이터
        """
        sql = """
        INSERT INTO crawled_community_posts (
            artist_id, platform, post_id, post_title, post_url,
            view_count, comment_count, posted_at, created_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
        ON CONFLICT (post_id)
        DO UPDATE SET
            view_count = EXCLUDED.view_count,
            comment_count = EXCLUDED.comment_count,
            updated_at = NOW()
        """
        
        self.db_cursor.execute(sql, (
            data['artist_id'],
            data['platform'],
            data['post_id'],
            data['post_title'],
            data['post_url'],
            data['view_count'],
            data['comment_count'],
            data['posted_at']
        ))
        
        self.db_conn.commit()
        print(f"💾 [{self.crawler_name}] DB 저장 완료: {data['post_id']}")


if __name__ == '__main__':
    # 테스트 실행
    crawler = CommunityCrawler()
    test_artist = {'id': 1, 'name': 'aespa'}
    crawler.run(test_artist)
