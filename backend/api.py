from fastapi import APIRouter
from models import Event
from session_manager import process_event
from datetime import datetime, timezone
from db import get_sessions_between
from pydantic import BaseModel
from datetime import datetime, timezone
from report_generator import generate_daily_report
from db import get_settings, save_settings
from pydantic import BaseModel
from leetcode.sync import sync_leetcode_sequential, sync_leetcode_concurrent
from db import get_settings
from leetcode.sync import maybe_sync_leetcode
from db import (
    get_leetcode_total_solved,
    get_leetcode_difficulty_counts,
    get_leetcode_recent,
    get_topic_last_seen
)
from leetcode.client import fetch_leetcode_calendar
from leetcode.suggestions import generate_topic_suggestions
import time
from leetcode.suggestions import generate_suggestions





class OverrideRequest(BaseModel):
    category: str


class SettingsRequest(BaseModel):
    report_time: str
    email: str
    telegram_chat_id: str
    enable_email: bool
    enable_telegram: bool


class SettingsRequest(BaseModel):
    report_time: str
    email: str
    telegram_chat_id: str
    enable_email: bool
    enable_telegram: bool
    leetcode_username: str


router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/event")
def receive_event(event: Event):
    process_event(event)
    print(event)
    return {"status": "ok"}



@router.get("/sessions/today")
def get_today_sessions():
    now = datetime.now(timezone.utc)

    start_of_day = datetime(
        year=now.year,
        month=now.month,
        day=now.day,
        tzinfo=timezone.utc
    )

    start_ts = int(start_of_day.timestamp())
    end_ts = int(now.timestamp())

    # sessions = get_sessions_between(0, 2000)
    sessions = get_sessions_between(start_ts,end_ts)
    for s in sessions:
        if s["user_category"]:
            s["category"] = s["user_category"]


    return sessions

@router.post("/sessions/{session_id}/override")
def override_category(session_id: int, req: OverrideRequest):
    from db import update_user_category
    update_user_category(session_id, req.category)
    return {"status": "ok"}



@router.get("/reports/daily")
def get_daily_report(date: str | None = None):
    if date is None:
        date = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    return generate_daily_report(date)


@router.get("/settings")
def fetch_settings():
    return get_settings()


@router.post("/settings")
def update_settings(req: SettingsRequest):
    save_settings(req.dict())
    return {"status": "ok"}


@router.post("/reports/send-now")
def send_now():
    from scheduler import generate_and_send_once
    generate_and_send_once()
    return {"status": "sent"}


@router.post("/leetcode/sync")
def leetcode_sync():
    settings = get_settings()
    username = settings.get("leetcode_username")

    if not username:
        return {"error": "leetcode_username not set"}

    # new_count = sync_leetcode_sequential(username)
    new_count = sync_leetcode_concurrent(username)
    return {
        "status": "ok",
        "new_records": new_count
    }


@router.post("/leetcode/sync-ui")
def leetcode_sync_ui():
    settings = get_settings()
    username = settings.get("leetcode_username")

    if not username:
        return {"error": "leetcode_username not set"}

    new_count = maybe_sync_leetcode(username, min_gap_sec=60) # for testing doing it 60 for prod would have it 300sec
    return {"status": "ok", "new_records": new_count}


@router.get("/leetcode/stats")
def leetcode_stats():
    return {
        "total_solved": get_leetcode_total_solved(),
        "difficulty_counts": get_leetcode_difficulty_counts()
    }


@router.get("/leetcode/recent")
def leetcode_recent():
    return get_leetcode_recent(10)


@router.get("/leetcode/topic-last-seen")
def leetcode_topic_last_seen():
    return get_topic_last_seen()

@router.get("/leetcode/calendar")
def leetcode_calendar(year: int):
    settings = get_settings()
    username = settings.get("leetcode_username")

    if not username:
        return {"error": "leetcode_username not set"}

    return fetch_leetcode_calendar(username, year)

# @router.get("/leetcode/suggestions")
# def leetcode_suggestions():
#     return generate_topic_suggestions()



@router.get("/leetcode/suggestions")
def leetcode_suggestions():
    return generate_suggestions()