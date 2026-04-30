"""
X (Twitter) Crawler
X 트렌드 및 멘션 데이터 수집
"""
from src.crawlers.base_crawler import BaseCrawler
from datetime import datetime


class XCrawler(BaseCrawler):
    """X (Twitter) 크롤러"""
    
    def __init__(self):
        super().__init__("X Crawler")
    
    def crawl(self, artist: dict):
        """
        X 트렌드 크롤링
        
        Args:
            artist: 아티스트 정보 {'id': 1, 'name': 'aespa', ...}
        
        Returns:
            dict: 크롤링 데이터
        """
        print(f"🔍 [{self.crawler_name}] {artist['name']} X 데이터 수집 중...")
        
        # TODO: 실제 X API 구현
        # 현재는 더미 데이터 반환
        data = {
            'artist_id': artist['id'],
            'tweet_id': 'dummy_tweet_123',
            'keyword': f"#{artist['name']}",
            'tweet_text': f"Amazing performance by {artist['name']}! 🔥",
            'author_username': 'test_user',
            'retweet_count': 500,
            'like_count': 2000,
            'reply_count': 50,
            'posted_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return data
    
    def save_to_db(self, data: dict):
        """
        PostgreSQL에 데이터 저장
        
        Args:
            data: 저장할 X 데이터
        """
        sql = """
        INSERT INTO crawled_x_tweets (
            artist_id, tweet_id, keyword, tweet_text, author_username,
            retweet_count, like_count, reply_count, posted_at, created_at
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        ON CONFLICT (tweet_id)
        DO UPDATE SET
            retweet_count = EXCLUDED.retweet_count,
            like_count = EXCLUDED.like_count,
            reply_count = EXCLUDED.reply_count,
            updated_at = NOW()
        """
        
        self.db_cursor.execute(sql, (
            data['artist_id'],
            data['tweet_id'],
            data['keyword'],
            data['tweet_text'],
            data['author_username'],
            data['retweet_count'],
            data['like_count'],
            data['reply_count'],
            data['posted_at']
        ))
        
        self.db_conn.commit()
        print(f"💾 [{self.crawler_name}] DB 저장 완료: {data['tweet_id']}")


if __name__ == '__main__':
    # 테스트 실행
    crawler = XCrawler()
    test_artist = {'id': 1, 'name': 'aespa'}
    crawler.run(test_artist)
