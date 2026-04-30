"""
SM AI Backend - FastAPI Application
PostgreSQL 데이터 읽기 → Gemini 분석 → MySQL 저장
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai
from db_connectors import get_postgres_connection, get_mysql_connection
import os
from dotenv import load_dotenv

load_dotenv()

# Gemini API 설정
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

# FastAPI 앱
app = FastAPI(
    title="SM Artist Insights API",
    description="K-POP 아티스트 SNS 데이터 분석 API",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    """헬스 체크"""
    return {
        "status": "ok",
        "service": "SM AI Backend",
        "version": "1.0.0"
    }


@app.get("/api/artists/{artist_id}/youtube/stats")
def get_youtube_stats(artist_id: int):
    """
    아티스트의 YouTube 통계 조회
    PostgreSQL에서 크롤링 데이터 읽기
    """
    try:
        conn = get_postgres_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                COUNT(*) as video_count,
                SUM(view_count) as total_views,
                SUM(like_count) as total_likes,
                SUM(comment_count) as total_comments
            FROM crawled_youtube_videos
            WHERE artist_id = %s
        """, (artist_id,))
        
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        
        return {
            "artist_id": artist_id,
            "video_count": result[0] or 0,
            "total_views": result[1] or 0,
            "total_likes": result[2] or 0,
            "total_comments": result[3] or 0
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/artists/{artist_id}/analyze")
async def analyze_artist(artist_id: int):
    """
    아티스트 SNS 데이터 AI 분석
    1. PostgreSQL에서 데이터 읽기
    2. Gemini로 감정/트렌드 분석
    3. MySQL에 결과 저장
    """
    try:
        # 1. PostgreSQL에서 최근 데이터 가져오기
        pg_conn = get_postgres_connection()
        pg_cursor = pg_conn.cursor()
        
        pg_cursor.execute("""
            SELECT title, description, view_count, like_count
            FROM crawled_youtube_videos
            WHERE artist_id = %s
            ORDER BY published_at DESC
            LIMIT 10
        """, (artist_id,))
        
        videos = pg_cursor.fetchall()
        pg_cursor.close()
        pg_conn.close()
        
        if not videos:
            raise HTTPException(status_code=404, detail="No data found")
        
        # 2. Gemini로 분석
        prompt = f"""
        다음 YouTube 비디오 데이터를 분석하여 다음을 제공하세요:
        1. 전체적인 감정 (긍정/중립/부정)
        2. 주요 트렌드
        3. 인기 요인
        
        데이터:
        {videos[:3]}  # 샘플 데이터만
        
        JSON 형식으로 답변하세요.
        """
        
        response = model.generate_content(prompt)
        ai_result = response.text
        
        # 3. MySQL에 결과 저장
        mysql_conn = get_mysql_connection()
        mysql_cursor = mysql_conn.cursor()
        
        mysql_cursor.execute("""
            INSERT INTO ai_analysis_results (
                artist_id, analysis_type, result, created_at
            ) VALUES (%s, %s, %s, NOW())
        """, (artist_id, 'youtube_sentiment', ai_result))
        
        mysql_conn.commit()
        mysql_cursor.close()
        mysql_conn.close()
        
        return {
            "artist_id": artist_id,
            "analysis": ai_result,
            "data_count": len(videos)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv('API_HOST', '0.0.0.0'),
        port=int(os.getenv('API_PORT', 8000)),
        reload=True
    )
