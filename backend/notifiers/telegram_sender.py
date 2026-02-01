import os
import requests

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"


def send_telegram(chat_id: str, text: str):
    url = f"{BASE_URL}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    requests.post(url, json=payload)
