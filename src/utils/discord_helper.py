import os
import requests
from dotenv import load_dotenv

load_dotenv()

def send_discord_alert(message: str, level: str = "INFO"):
    """
    Discord 채널로 알림 전송
    level: 'INFO', 'ERROR'
    """
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    if not webhook_url:
        print("Warning: DISCORD_WEBHOOK_URL이 설정되지 않았습니다.")
        return

    prefix = "[ERROR]" if level == "ERROR" else "[INFO]"
    payload = {"content": f"{prefix} {message}"}

    try:
        response = requests.post(webhook_url, json=payload, timeout=5)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to send Discord alert: {e}")