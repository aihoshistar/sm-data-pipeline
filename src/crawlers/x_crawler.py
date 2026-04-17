from src.crawlers.base_crawler import BaseCrawler

class XCrawler(BaseCrawler):
    def __init__(self):
        super().__init__(platform_name="X(Twitter)")

    def crawl(self, artist_info: dict) -> dict:
        # TODO: 트위터 API 또는 크롤링 로직 구현
        return {
            "artist_id": artist_info['id'],
            "hashtag": f"#{artist_info['name']}",
            "tweet_count": 12500,
            "sample_tweets": "컴백 너무 기대된다! | 이번 컨셉 미쳤음"
        }

    def save_to_db(self, data: dict):
        cursor = self.db_conn.cursor()
        sql = """
            INSERT INTO sns_x_trends 
            (artist_id, hashtag, tweet_count, sample_tweets, collected_at)
            VALUES (%s, %s, %s, %s, NOW())
        """
        cursor.execute(sql, (
            data['artist_id'], data['hashtag'], data['tweet_count'], data['sample_tweets']
        ))
        self.db_conn.commit()
        cursor.close()