from pydantic import BaseModel

class Event(BaseModel):
    url: str
    domain: str
    title: str
    timestamp: int

class Session(BaseModel):
    url: str
    domain: str
    title: str
    start_time: int
    end_time: int
    duration_sec: int
