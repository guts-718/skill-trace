from fastapi import APIRouter
from models import Event
from session_manager import process_event

router = APIRouter()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/event")
def receive_event(event: Event):
    process_event(event)
    return {"status": "ok"}
