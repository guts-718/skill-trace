import time
import os
import requests
from db import save_settings, get_settings


BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

last_update_id = 0


def telegram_listener_loop():
    global last_update_id
    print("Telegram listener started")

    while True:
        try:
            resp = requests.get(
                f"{BASE_URL}/getUpdates?offset={last_update_id + 1}"
            ).json()

            for update in resp.get("result", []):
                last_update_id = update["update_id"]

                msg = update.get("message")
                if not msg:
                    continue

                text = msg.get("text", "")
                chat_id = msg["chat"]["id"]

                if text == "/start":
                    save_settings({
                        "report_time": get_settings()["report_time"],
                        "email": get_settings()["email"],
                        "telegram_chat_id": str(chat_id),
                        "enable_email": get_settings()["enable_email"],
                        "enable_telegram": True
                    })

                    requests.post(
                        f"{BASE_URL}/sendMessage",
                        json={
                            "chat_id": chat_id,
                            "text": "✅ SkillTrace connected. You will receive daily reports here."
                        }
                    )

        except Exception as e:
            print("Telegram listener error:", e)

        time.sleep(5)
