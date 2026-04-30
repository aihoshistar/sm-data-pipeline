"""
Discord Webhook Helper
크롤링 결과 및 에러 알림
"""
import os
import requests
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()


def send_discord_message(message: str, status: str = "info"):
    """
    Discord Webhook으로 메시지 전송
    
    Args:
        message: 전송할 메시지
        status: 메시지 상태 (info, success, error)
    """
    webhook_url = os.getenv('DISCORD_WEBHOOK_URL')
    
    if not webhook_url:
        print("⚠️  Discord Webhook URL이 설정되지 않았습니다.")
        return
    
    # 상태에 따른 색상
    colors = {
        "info": 0x3498db,     # 파란색
        "success": 0x2ecc71,  # 초록색
        "error": 0xe74c3c     # 빨간색
    }
    
    # 상태에 따른 이모지
    emojis = {
        "info": "ℹ️",
        "success": "✅",
        "error": "❌"
    }
    
    embed = {
        "title": f"{emojis.get(status, 'ℹ️')} SM Data Pipeline",
        "description": message,
        "color": colors.get(status, 0x3498db),
        "timestamp": datetime.utcnow().isoformat(),
        "footer": {
            "text": "SM Artist Insights"
        }
    }
    
    data = {
        "embeds": [embed]
    }
    
    try:
        response = requests.post(webhook_url, json=data)
        if response.status_code == 204:
            print("✅ Discord 알림 전송 성공")
        else:
            print(f"⚠️  Discord 알림 전송 실패: {response.status_code}")
    except Exception as e:
        print(f"❌ Discord 알림 전송 에러: {e}")


def send_crawling_success(crawler_name: str, count: int):
    """크롤링 성공 알림"""
    message = f"**{crawler_name}** 크롤링 완료\n📊 수집 데이터: {count}건"
    send_discord_message(message, "success")


def send_crawling_error(crawler_name: str, error: str):
    """크롤링 에러 알림"""
    message = f"**{crawler_name}** 크롤링 실패\n⚠️ 에러: {error}"
    send_discord_message(message, "error")


if __name__ == '__main__':
    # 테스트
    send_discord_message("Discord 연동 테스트", "info")
