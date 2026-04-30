# SM Data Pipeline

Airflow 기반 SNS 데이터 수집 파이프라인. YouTube, X(Twitter), 커뮤니티 크롤링 → PostgreSQL 저장.

## Tech Stack

- Apache Airflow 2.10
- PostgreSQL (데이터 저장)
- Python 3.10
- Selenium, BeautifulSoup

## Quick Start

### Docker로 실행 (권장)

```bash
# 루트 디렉토리에서
cd sm-artist-insights
./scripts/start.sh
```

Airflow UI: http://localhost:8081 (admin/admin)

### 로컬 개발

```bash
# 의존성 설치
python3 -m venv venv 
source venv/bin/activate 
# google-re2 패키지를 설치하기 위해서는 abseil 가 필요함
brew install abseil
brew install re2
pip install pybind11
pip install google-re2
pip install -r requirements.txt

# 환경변수 설정
cp .env.example .env
nano .env

# Airflow 실행
airflow standalone
```

## 디렉토리 구조

```
sm-data-pipeline/
├── dags/                    # Airflow DAG 파일
│   ├── youtube_collect_dag.py
│   ├── x_trend_collect_dag.py
│   └── community_collect_dag.py
├── src/
│   ├── crawlers/           # 크롤러 구현
│   ├── connectors/         # DB 연결
│   └── utils/              # Discord 알림 등
└── requirements.txt
```

## 주요 기능

- **YouTube 크롤러**: 영상 조회수, 좋아요, 댓글 수집
- **X 크롤러**: 트윗, 해시태그, 멘션 수집
- **커뮤니티 크롤러**: 더쿠, 인스티즈 게시글 수집
- **자동 스케줄링**: Cron 기반 주기적 실행
- **Discord 알림**: 크롤링 성공/실패 알림

## 환경변수

```bash
# PostgreSQL
POSTGRES_HOST=postgres
POSTGRES_PASSWORD=your_password

# API 키 (선택)
YOUTUBE_API_KEY=your_key
X_BEARER_TOKEN=your_token

# Discord
DISCORD_WEBHOOK_URL=your_webhook_url
```

## 상세 문서

전체 프로젝트 구조 및 설정: [루트 README](../README.md)