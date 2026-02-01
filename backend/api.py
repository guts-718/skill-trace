from fastapi import APIRouter
from models import Event
from session_manager import process_event
from datetime import datetime, timezone
from db import get_sessions_between
from pydantic import BaseModel

class OverrideRequest(BaseModel):
    category: str


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

