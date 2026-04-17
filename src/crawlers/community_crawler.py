from src.crawlers.base_crawler import BaseCrawler

class CommunityCrawler(BaseCrawler):
    def __init__(self):
        super().__init__(platform_name="Community")

    def crawl(self, artist_info: dict) -> dict:
        # TODO: 더쿠, 인스티즈 등 커뮤니티 크롤링 로직 구현
        return {
            "artist_id": artist_info['id'],
            "platform": "theqoo",
            "post_title": f"{artist_info['name']} 오늘 뜬 티저 사진",
            "post_content": "분위기 대박이다 진짜...",
            "view_count": 8500
        }

    def save_to_db(self, data: dict):
        cursor = self.db_conn.cursor()
        sql = """
            INSERT INTO sns_community_posts 
            (artist_id, platform, post_title, post_content, view_count, post_created_at, collected_at)
            VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
        """
        cursor.execute(sql, (
            data['artist_id'], data['platform'], data['post_title'], 
            data['post_content'], data['view_count']
        ))
        self.db_conn.commit()
        cursor.close()