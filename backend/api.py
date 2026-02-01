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


class OverrideRequest(BaseModel):
    category: str


class SettingsRequest(BaseModel):
    report_time: str
    email: str
    telegram_chat_id: str
    enable_email: bool
    enable_telegram: bool


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
