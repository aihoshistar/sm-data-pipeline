# SM Data Pipeline

K-POP 아티스트 SNS 데이터 수집 파이프라인 (Apache Airflow)

## 📋 프로젝트 개요

SM Entertainment 소속 아티스트들의 SNS 데이터를 자동으로 수집하는 Airflow 기반 데이터 파이프라인입니다.

### 수집 데이터
- **YouTube**: 비디오 조회수, 좋아요, 댓글
- **X (Twitter)**: 트렌드, 멘션, 리트윗
- **커뮤니티**: 더쿠, 인스티즈 게시글

## 아키텍처

```
Airflow Scheduler
  ↓
DAGs (3개)
  ├─ YouTube Collection (매일 자정)
  ├─ X Trend Collection (2시간마다)
  └─ Community Collection (6시간마다)
  ↓
Crawlers (Python)
  ↓
PostgreSQL (sm_crawled_data)
```

## 시작

### Docker 환경 (권장)

```bash
# 1. Docker Compose 시작
cd ../sm-artist-insights
docker-compose up -d

# 2. Airflow UI 접속
open http://localhost:8081
# ID: admin, PW: admin

# 3. DAG 수동 실행
docker exec sm-airflow airflow dags trigger youtube_data_collection_dag
```

### 로컬 개발 (테스트만)

```bash
# 1. venv 생성
python3 -m venv venv
source venv/bin/activate

# 2. 개발 의존성 설치
pip install --upgrade pip
pip install -r requirements-dev.txt

# 3. 테스트 실행
pytest tests/ -v
```

## 의존성

### Docker용 (requirements.txt)
- apache-airflow==2.9.3
- psycopg2-binary==2.9.9
- selenium==4.20.0
- beautifulsoup4==4.12.3

### 로컬 테스트용 (requirements-dev.txt)
- pytest==8.3.4
- 위 패키지들 (Airflow 제외)

## 프로젝트 구조

```
sm-data-pipeline/
├── requirements.txt          # Docker용
├── requirements-dev.txt      # 로컬 테스트용
├── Dockerfile
├── .env.example
├── dags/                     # Airflow DAG
│   ├── youtube_collect_dag.py
│   ├── x_trend_collect_dag.py
│   └── community_collect_dag.py
├── src/                      # 소스 코드
│   ├── connectors/
│   │   └── db_connector.py
│   ├── crawlers/
│   │   ├── base_crawler.py
│   │   ├── youtube_crawler.py
│   │   ├── x_crawler.py
│   │   └── community_crawler.py
│   └── utils/
│       └── discord_helper.py
└── tests/                    # 테스트
    └── test_crawlers.py
```

## 환경 변수

`.env` 파일 생성:

```bash
cp .env.example .env
```

필수 설정:
- `POSTGRES_HOST`: PostgreSQL 호스트
- `POSTGRES_PASSWORD`: PostgreSQL 비밀번호
- `YOUTUBE_API_KEY`: YouTube Data API 키 (선택)
- `X_BEARER_TOKEN`: X API Bearer Token (선택)
- `DISCORD_WEBHOOK_URL`: Discord 알림 (선택)

## 테스트

```bash
# 전체 테스트
pytest tests/ -v

# 커버리지 포함
pytest tests/ --cov=src --cov-report=html

# 특정 크롤러만
pytest tests/test_crawlers.py::TestYoutubeCrawler -v
```

## 데이터베이스 스키마

### crawled_youtube_videos
```sql
CREATE TABLE crawled_youtube_videos (
    id SERIAL PRIMARY KEY,
    artist_id INT NOT NULL,
    video_id VARCHAR(100) UNIQUE NOT NULL,
    title TEXT,
    view_count BIGINT,
    like_count BIGINT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### crawled_x_tweets
```sql
CREATE TABLE crawled_x_tweets (
    id SERIAL PRIMARY KEY,
    artist_id INT NOT NULL,
    tweet_id VARCHAR(100) UNIQUE NOT NULL,
    keyword VARCHAR(100),
    tweet_text TEXT,
    retweet_count INT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### crawled_community_posts
```sql
CREATE TABLE crawled_community_posts (
    id SERIAL PRIMARY KEY,
    artist_id INT NOT NULL,
    platform VARCHAR(50),
    post_id VARCHAR(100) UNIQUE NOT NULL,
    post_title TEXT,
    view_count INT,
    created_at TIMESTAMP DEFAULT NOW()
);
```

## 개발 가이드

자세한 내용은 [LOCAL_DEVELOPMENT.md](LOCAL_DEVELOPMENT.md) 참고

### 역할 분리
- **Docker**: Airflow 운영 환경
- **로컬 venv**: 크롤러 테스트만

### 개발 워크플로우
1. 로컬에서 크롤러 코드 작성
2. pytest로 테스트
3. Docker로 DAG 실행 확인
4. Git 커밋

## TODO

- [ ] YouTube Data API v3 연동
- [ ] X API v2 연동
- [ ] Selenium 커뮤니티 크롤링 구현
- [ ] Discord 알림 연동
- [ ] CI/CD 파이프라인
