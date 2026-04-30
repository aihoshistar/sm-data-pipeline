"""
SM Data Pipeline - Crawler Tests
로컬 환경에서 크롤러 로직 테스트
"""
import pytest
from unittest.mock import Mock, patch
import sys
from pathlib import Path

# src 경로 추가
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from connectors.db_connector import get_db_connection
from crawlers.youtube_crawler import YoutubeCrawler
from crawlers.x_crawler import XCrawler
from crawlers.community_crawler import CommunityCrawler


class TestDatabaseConnector:
    """DB 커넥터 테스트"""
    
    @patch('psycopg2.connect')
    def test_get_db_connection(self, mock_connect):
        """PostgreSQL 연결 테스트"""
        mock_connect.return_value = Mock()
        
        conn = get_db_connection()
        
        assert conn is not None
        mock_connect.assert_called_once()


class TestYoutubeCrawler:
    """YouTube 크롤러 테스트"""
    
    @patch('crawlers.base_crawler.get_db_connection')
    def test_crawl_returns_data(self, mock_db):
        """크롤링 데이터 반환 테스트"""
        mock_db.return_value = Mock()
        
        crawler = YoutubeCrawler()
        artist = {'id': 1, 'name': 'aespa'}
        
        data = crawler.crawl(artist)
        
        assert data is not None
        assert data['artist_id'] == 1
        assert 'video_id' in data
        assert 'view_count' in data
        assert 'like_count' in data
    
    @patch('crawlers.base_crawler.get_db_connection')
    def test_save_to_db(self, mock_db):
        """DB 저장 테스트"""
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_conn.cursor.return_value = mock_cursor
        mock_db.return_value = mock_conn
        
        crawler = YoutubeCrawler()
        data = {
            'artist_id': 1,
            'video_id': 'test123',
            'title': 'Test Video',
            'description': 'Test Description',
            'thumbnail_url': 'http://test.com/thumb.jpg',
            'view_count': 1000,
            'like_count': 100,
            'comment_count': 10,
            'published_at': '2024-01-01 00:00:00'
        }
        
        crawler.save_to_db(data)
        
        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()


class TestXCrawler:
    """X(Twitter) 크롤러 테스트"""
    
    @patch('crawlers.base_crawler.get_db_connection')
    def test_crawl_returns_data(self, mock_db):
        """크롤링 데이터 반환 테스트"""
        mock_db.return_value = Mock()
        
        crawler = XCrawler()
        artist = {'id': 1, 'name': 'aespa'}
        
        data = crawler.crawl(artist)
        
        assert data is not None
        assert data['artist_id'] == 1
        assert 'keyword' in data
        assert 'tweet_text' in data


class TestCommunityCrawler:
    """커뮤니티 크롤러 테스트"""
    
    @patch('crawlers.base_crawler.get_db_connection')
    def test_crawl_returns_data(self, mock_db):
        """크롤링 데이터 반환 테스트"""
        mock_db.return_value = Mock()
        
        crawler = CommunityCrawler()
        artist = {'id': 1, 'name': 'aespa'}
        
        data = crawler.crawl(artist)
        
        assert data is not None
        assert data['artist_id'] == 1
        assert data['platform'] == 'theqoo'
        assert 'post_title' in data


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
