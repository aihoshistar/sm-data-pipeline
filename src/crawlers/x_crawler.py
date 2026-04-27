"""
X (Twitter) Crawler
X(트위터) 트렌드 크롤링
"""
from crawlers.base_crawler import BaseCrawler


class XCrawler(BaseCrawler):
    """X(트위터) 트렌드 크롤러"""
    
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
            "keyword": artist_info['name'],  # hashtag → keyword (스키마 일치)
            "tweet_count": 12500,
            "sentiment_score": 0.75,  # -1.0 ~ 1.0 (추가)
            "top_hashtags": f"#{artist_info['name']}, #KPOP, #comeback"  # sample_tweets → top_hashtags
        }

    def save_to_db(self, data: dict):
        """
        X 트렌드를 sns_x_trends 테이블에 저장
        
        Args:
            data: X 트렌드 데이터
        """
        cursor = self.db_conn.cursor()
        
        # 테이블 스키마와 일치하도록 수정
        sql = """
            INSERT INTO sns_x_trends 
            (artist_id, keyword, tweet_count, sentiment_score, top_hashtags, collected_at)
            VALUES (%s, %s, %s, %s, %s, NOW())
        """
        
        cursor.execute(sql, (
            data['artist_id'],
            data['keyword'],  # hashtag → keyword
            data['tweet_count'],
            data.get('sentiment_score', 0.0),  # 없으면 0.0
            data['top_hashtags']  # sample_tweets → top_hashtags
        ))
        
        self.db_conn.commit()
        cursor.close()
        
        print(f"✅ X 트렌드 저장: keyword={data['keyword']}, tweets={data['tweet_count']:,}")


# 테스트용
if __name__ == "__main__":
    crawler = XCrawler()
    
    # 테스트 아티스트 정보
    test_artist = {
        'id': 1,
        'name': 'aespa'
    }
    
    # 크롤링 실행
    crawler.execute(test_artist)
