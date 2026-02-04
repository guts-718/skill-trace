import time
import requests
import psutil
import pygetwindow as gw

BACKEND_URL = "http://localhost:8000/event"
POLL_INTERVAL = 2  # seconds

last_signature = None


def get_active_window_info():
    try:
        win = gw.getActiveWindow()
        if not win:
            return None

        title = win.title or ""

        pid = win._hWnd  # fallback identifier
        app_name = "unknown"

        try:
            proc = psutil.Process(win._getWindowPID())
            app_name = proc.name()
        except Exception:
            pass

        return {
            "app": app_name,
            "title": title
        }
    except Exception:
        return None


def send_event(info):
    payload = {
        "source": "desktop",
        "app": info["app"],
        "title": info["title"],
        "timestamp": int(time.time())
    }
    print("payload: ", payload)

    try:
        requests.post(BACKEND_URL, json=payload, timeout=5)
    except Exception:
        pass


def main():
    global last_signature

    print("Desktop watcher started...")

    while True:
        info = get_active_window_info()

        if info:
            signature = f'{info["app"]}|{info["title"]}'

            if signature != last_signature:
                last_signature = signature
                send_event(info)

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()
