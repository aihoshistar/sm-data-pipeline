"""
Community Crawler - PostgreSQL
커뮤니티 게시글 크롤링 (PostgreSQL에 저장)
"""
from crawlers.base_crawler import BaseCrawler


class CommunityCrawler(BaseCrawler):
    """커뮤니티 게시글 크롤러 (PostgreSQL)"""
    
    def __init__(self):
        super().__init__(platform_name="Community")

    def crawl(self, artist_info: dict) -> dict:
        """
        커뮤니티 게시글 크롤링
        
        TODO: 더쿠(theqoo), 인스티즈(instiz), 판(pann) 등 크롤링 구현
        
        Args:
            artist_info: 아티스트 정보
        
        Returns:
            커뮤니티 게시글 데이터
        """
        # 현재는 임시 더미 데이터 반환
        # 실제 구현 시 BeautifulSoup 또는 Selenium으로 크롤링
        
        return {
            "artist_id": artist_info['id'],
            "platform": "theqoo",  # theqoo, instiz, pann 등
            "post_url": "https://theqoo.net/square/123456789",
            "post_title": f"{artist_info['name']} 오늘 뜬 티저 사진",
            "post_content": "분위기 대박이다 진짜... 이번 컨셉 미쳤음 완전 기대됨",
            "author_nickname": "케이팝덕후",
            "view_count": 12500,
            "like_count": 1850,
            "comment_count": 234
        }

    def save_to_db(self, data: dict):
        """
        커뮤니티 게시글을 crawled_community_posts 테이블에 저장 (PostgreSQL)
        
        Args:
            data: 커뮤니티 게시글 데이터
        """
        cursor = self.db_conn.cursor()
        
        # PostgreSQL 테이블: crawled_community_posts
        sql = """
            INSERT INTO crawled_community_posts 
            (artist_id, platform, post_url, post_title, post_content, 
             author_nickname, view_count, like_count, comment_count, crawled_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
        """
        
        cursor.execute(sql, (
            data['artist_id'],
            data['platform'],
            data.get('post_url', ''),
            data['post_title'],
            data['post_content'],
            data.get('author_nickname', 'unknown'),
            data.get('view_count', 0),
            data.get('like_count', 0),
            data.get('comment_count', 0)
        ))
        
        self.db_conn.commit()
        cursor.close()
        
        print(f"✅ 커뮤니티 게시글 저장 (PostgreSQL): platform={data['platform']}, likes={data.get('like_count', 0):,}")


# 테스트용
if __name__ == "__main__":
    crawler = CommunityCrawler()
    
    test_artist = {
        'id': 1,
        'name': 'aespa'
    }
    
    crawler.execute(test_artist)
