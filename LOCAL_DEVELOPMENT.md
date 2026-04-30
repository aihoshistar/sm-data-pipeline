# SM Data Pipeline - 로컬 개발 가이드

## 역할 분리

| 환경 | 역할 | 사용 |
|------|------|------|
| **Docker** | Airflow 운영 환경 | DAG 실행, 스케줄링 |
| **로컬 venv** | 크롤러 테스트 | 단위 테스트, 로직 검증 |

---

## Docker 환경 (Airflow 실행)

### 1. 서비스 시작

```bash
# 루트 디렉토리에서
cd sm-artist-insights
./scripts/start.sh
```

### 2. Airflow UI 접속

```
http://localhost:8081
ID: admin
PW: admin
```

### 3. DAG 수동 실행

```bash
docker exec sm-airflow airflow dags trigger youtube_data_collection_dag
```

### 4. 로그 확인

```bash
docker logs -f sm-airflow
```

---

## 🐍 로컬 venv (테스트 실행)

### 1. 환경 설정 (최초 1회)

```bash
cd sm-data-pipeline

# venv 생성
python3 -m venv venv
source venv/bin/activate

# 개발 의존성 설치 (Airflow 제외)
pip install --upgrade pip
pip install -r requirements-dev.txt
```

### 2. 테스트 실행

```bash
# 전체 테스트
pytest tests/ -v

# 특정 테스트만
pytest tests/test_crawlers.py::TestYoutubeCrawler -v

# 커버리지 포함
pytest tests/ --cov=src --cov-report=html
```

### 3. 크롤러 단독 테스트

```bash
# YouTube 크롤러
python src/crawlers/youtube_crawler.py

# X 크롤러
python src/crawlers/x_crawler.py

# 커뮤니티 크롤러
python src/crawlers/community_crawler.py
```

---

## 파일 구조

```
sm-data-pipeline/
├── requirements.txt          # Docker용 (Airflow 포함)
├── requirements-dev.txt      # 로컬용 (테스트만)
├── Dockerfile               # Docker 이미지 빌드
├── dags/                    # Airflow DAG 파일
│   ├── youtube_collect_dag.py
│   ├── x_trend_collect_dag.py
│   └── community_collect_dag.py
├── src/                     # 크롤러 소스
│   ├── crawlers/
│   │   ├── base_crawler.py
│   │   ├── youtube_crawler.py
│   │   ├── x_crawler.py
│   │   └── community_crawler.py
│   ├── connectors/
│   │   └── db_connector.py
│   └── utils/
│       └── discord_helper.py
└── tests/                   # 로컬 테스트
    ├── __init__.py
    └── test_crawlers.py
```

---

## 개발 워크플로우

### 1. 로컬에서 크롤러 개발

```bash
# 1. 코드 작성
vim src/crawlers/youtube_crawler.py

# 2. 테스트
pytest tests/test_crawlers.py -v

# 3. 단독 실행 확인
python src/crawlers/youtube_crawler.py
```

### 2. Docker에서 DAG 테스트

```bash
# 1. Docker 재시작 (코드 변경 반영)
docker-compose restart airflow

# 2. DAG 수동 실행
docker exec sm-airflow airflow dags trigger youtube_data_collection_dag

# 3. 로그 확인
docker logs --tail 100 sm-airflow
```

### 3. 코드 커밋

```bash
git add .
git commit -m "feat: YouTube 크롤러 구현"
git push
```

---

## 테스트 작성 예시

```python
# tests/test_crawlers.py

import pytest
from unittest.mock import Mock, patch
from src.crawlers.youtube_crawler import YoutubeCrawler

@patch('src.crawlers.base_crawler.get_db_connection')
def test_youtube_crawler(mock_db):
    """YouTube 크롤러 테스트"""
    mock_db.return_value = Mock()
    
    crawler = YoutubeCrawler()
    artist = {'id': 1, 'name': 'aespa'}
    
    data = crawler.crawl(artist)
    
    assert data['artist_id'] == 1
    assert 'video_id' in data
    assert data['view_count'] > 0
```

---

## 환경변수 설정

### 로컬 테스트용 .env

```bash
# sm-data-pipeline/.env.local
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password123
POSTGRES_DB=sm_crawled_data

DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
```

### 테스트 시 로드

```python
# tests/conftest.py
import os
from dotenv import load_dotenv

load_dotenv('.env.local')
```

---

## 트러블슈팅

### Q: 로컬에서 DB 연결 안 됨
```bash
# Docker PostgreSQL에 로컬에서 접속
docker exec -it sm-postgres psql -U postgres -d sm_crawled_data
```

### Q: 테스트 실패
```bash
# Mock 사용으로 실제 DB 없이 테스트
pytest tests/ -v --tb=short
```

### Q: Import 에러
```bash
# PYTHONPATH 설정
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
pytest tests/
```

---

## 권장 개발 환경

### VSCode 설정

```json
// .vscode/settings.json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["tests"],
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true
}
```

### VSCode 확장 프로그램

- Python
- Pylance
- Docker
- Remote - Containers

---

## 체크리스트

### 로컬 개발 시작
- [ ] `python3 -m venv venv`
- [ ] `source venv/bin/activate`
- [ ] `pip install -r requirements-dev.txt`
- [ ] `pytest tests/ -v`

### 코드 변경 후
- [ ] 로컬 테스트 통과: `pytest tests/`
- [ ] Docker 재시작: `docker-compose restart airflow`
- [ ] DAG 수동 실행 확인
- [ ] Git 커밋

---

## 정리

**로컬 (venv):**
- 크롤러 로직 작성
- 단위 테스트 실행
- 빠른 개발 반복

**Docker:**
- Airflow 전체 실행
- DAG 스케줄링
- 운영 환경 테스트
