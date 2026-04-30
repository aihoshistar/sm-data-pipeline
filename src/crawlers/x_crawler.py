"""
X (Twitter) Crawler - PostgreSQL
X(트위터) 트렌드 크롤링 (PostgreSQL에 저장)
"""
from crawlers.base_crawler import BaseCrawler


class XCrawler(BaseCrawler):
    """X(트위터) 트렌드 크롤러 (PostgreSQL)"""
    
    def __init__(self):
        super().__init__(platform_name="X(Twitter)")

    def crawl(self, artist_info: dict) -> dict:
        """
        X(트위터) 트렌드 크롤링
        
        TODO: X API v2 또는 크롤링 로직 구현
        
        Args:
            artist_info: 아티스트 정보
        
        Returns:
            X 트렌드 데이터
        """
        # 현재는 임시 더미 데이터 반환
        # 실제 구현 시 X API 또는 크롤링 로직으로 대체
        
        return {
            "artist_id": artist_info['id'],
            "keyword": artist_info['name'],
            "tweet_text": f"{artist_info['name']} 컴백 대박! 이번 노래 진짜 좋다 #KPOP #{artist_info['name']}",
            "tweet_url": f"https://twitter.com/dummy/status/123456789",
            "author_username": "kpop_fan_123",
            "retweet_count": 1250,
            "like_count": 3500,
            "reply_count": 180
        }

    def save_to_db(self, data: dict):
        """
        X 트렌드를 crawled_x_tweets 테이블에 저장 (PostgreSQL)
        
        Args:
            data: X 트렌드 데이터
        """
        cursor = self.db_conn.cursor()
        
        # PostgreSQL 테이블: crawled_x_tweets
        sql = """
            INSERT INTO crawled_x_tweets 
            (artist_id, keyword, tweet_text, tweet_url, author_username, 
             retweet_count, like_count, reply_count, crawled_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """
        
        cursor.execute(sql, (
            data['artist_id'],
            data['keyword'],
            data['tweet_text'],
            data.get('tweet_url', ''),
            data.get('author_username', 'unknown'),
            data.get('retweet_count', 0),
            data.get('like_count', 0),
            data.get('reply_count', 0)
        ))
        
        self.db_conn.commit()
        cursor.close()
        
        print(f"✅ X 트렌드 저장 (PostgreSQL): keyword={data['keyword']}, likes={data.get('like_count', 0):,}")


# 테스트용
if __name__ == "__main__":
    crawler = XCrawler()
    
    test_artist = {
        'id': 1,
        'name': 'aespa'
    }
    
    crawler.execute(test_artist)
