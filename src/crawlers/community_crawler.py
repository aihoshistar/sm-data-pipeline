"""
Community Crawler
커뮤니티 게시글 크롤링
"""
from crawlers.base_crawler import BaseCrawler
from datetime import datetime


class CommunityCrawler(BaseCrawler):
    """커뮤니티 게시글 크롤러"""
    
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
            "platform": "theqoo",  # theqoo, instiz, pann, reddit 등
            "post_title": f"{artist_info['name']} 오늘 뜬 티저 사진",
            "post_content": "분위기 대박이다 진짜... 이번 컨셉 미쳤음",
            "like_count": 1850,  # view_count → like_count (스키마 일치)
            "comment_count": 234,  # 추가
            "posted_at": datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # post_created_at → posted_at
        }

    def save_to_db(self, data: dict):
        """
        커뮤니티 게시글을 sns_community_posts 테이블에 저장
        
        Args:
            data: 커뮤니티 게시글 데이터
        """
        cursor = self.db_conn.cursor()
        
        # 테이블 스키마와 일치하도록 수정
        sql = """
            INSERT INTO sns_community_posts 
            (artist_id, platform, post_title, post_content, like_count, comment_count, posted_at, collected_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
        """
        
        cursor.execute(sql, (
            data['artist_id'],
            data['platform'],
            data['post_title'],
            data['post_content'],
            data.get('like_count', 0),  # 없으면 0
            data.get('comment_count', 0),  # 없으면 0
            data['posted_at']  # post_created_at → posted_at
        ))
        
        self.db_conn.commit()
        cursor.close()
        
        print(f"✅ 커뮤니티 게시글 저장: platform={data['platform']}, likes={data.get('like_count', 0):,}")


# 테스트용
if __name__ == "__main__":
    crawler = CommunityCrawler()
    
    # 테스트 아티스트 정보
    test_artist = {
        'id': 1,
        'name': 'aespa'
    }
    
    # 크롤링 실행
    crawler.execute(test_artist)
