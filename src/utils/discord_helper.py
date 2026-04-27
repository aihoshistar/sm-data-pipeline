"""
Discord Helper
Discord 웹훅을 통한 알림 전송
"""
import os
import requests
from dotenv import load_dotenv

load_dotenv()


def send_discord_alert(message: str, level: str = "INFO"):
    """
    Discord 채널로 알림 전송
    
    Args:
        message: 전송할 메시지
        level: 알림 레벨 ('INFO', 'WARNING', 'ERROR')
    
    Returns:
        성공 여부 (True/False)
    """
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    
    if not webhook_url:
        print("⚠️ Warning: DISCORD_WEBHOOK_URL이 설정되지 않았습니다.")
        return False

    # 레벨에 따른 이모지 및 색상
    emoji_map = {
        "INFO": "ℹ️",
        "WARNING": "⚠️",
        "ERROR": "🚨"
    }
    
    emoji = emoji_map.get(level.upper(), "📌")
    prefix = f"{emoji} [{level.upper()}]"
    
    payload = {
        "content": f"{prefix} {message}",
        "username": "SM Artist Insights Bot"
    }

    try:
        response = requests.post(webhook_url, json=payload, timeout=5)
        response.raise_for_status()
        print(f"✅ Discord 알림 전송 성공: {level}")
        return True
        
    except requests.exceptions.Timeout:
        print(f"❌ Discord 알림 타임아웃: {message[:50]}...")
        return False
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Discord 알림 전송 실패: {e}")
        return False


def send_discord_embed(title: str, description: str, color: int = 0x00FF00, fields: list = None):
    """
    Discord 임베드 메시지 전송 (더 예쁜 형식)
    
    Args:
        title: 임베드 제목
        description: 임베드 설명
        color: 임베드 색상 (HEX)
        fields: 추가 필드 리스트
    
    Returns:
        성공 여부 (True/False)
    """
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    
    if not webhook_url:
        print("⚠️ Warning: DISCORD_WEBHOOK_URL이 설정되지 않았습니다.")
        return False

    embed = {
        "title": title,
        "description": description,
        "color": color,
        "fields": fields or [],
        "footer": {
            "text": "SM Artist Insights"
        }
    }
    
    payload = {
        "embeds": [embed],
        "username": "SM Artist Insights Bot"
    }

    try:
        response = requests.post(webhook_url, json=payload, timeout=5)
        response.raise_for_status()
        print(f"✅ Discord 임베드 전송 성공")
        return True
        
    except Exception as e:
        print(f"❌ Discord 임베드 전송 실패: {e}")
        return False


# 테스트용
if __name__ == "__main__":
    # 기본 알림 테스트
    send_discord_alert("테스트 메시지입니다.", level="INFO")
    
    # 임베드 알림 테스트
    send_discord_embed(
        title="크롤링 완료",
        description="aespa 데이터 수집이 완료되었습니다.",
        color=0x00FF00,
        fields=[
            {"name": "플랫폼", "value": "YouTube", "inline": True},
            {"name": "수집 개수", "value": "15개", "inline": True}
        ]
    )
