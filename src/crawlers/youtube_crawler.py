from src.crawlers.base_crawler import BaseCrawler

class YoutubeCrawler(BaseCrawler):
    def __init__(self):
        super().__init__(platform_name="YouTube")

    def crawl(self, artist_info: dict) -> dict:
        # TODO: Selenium 또는 BeautifulSoup을 사용한 크롤링 기능 구현
        # 현재는 임시 더미 데이터 반환
        return {
            "artist_id": artist_info['id'],
            "video_id": "dummy_video_123",
            "video_title": f"{artist_info['name']} - 신곡 MV",
            "view_count": 5000000,
            "like_count": 250000,
            "comment_count": 15000,
            "top_comments": "노래 좋아요 | 글로벌 진출 가자 | I love this song"
        }

    def save_to_db(self, data: dict):
        cursor = self.db_conn.cursor()
        sql = """
            INSERT INTO sns_youtube_stats 
            (artist_id, video_id, video_title, view_count, like_count, comment_count, top_comments, collected_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
        """
        cursor.execute(sql, (
            data['artist_id'], data['video_id'], data['video_title'],
            data['view_count'], data['like_count'], data['comment_count'], data['top_comments']
        ))
        self.db_conn.commit()
        cursor.close()