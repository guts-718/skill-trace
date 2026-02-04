from pydantic import BaseModel

from typing import Optional
from pydantic import BaseModel

class Event(BaseModel):
    source: str

    # browser fields
    url: Optional[str] = None
    domain: Optional[str] = None

    # desktop fields
    app: Optional[str] = None

    # common
    title: Optional[str] = None
    referrer: Optional[str] = None
    timestamp: int


class Session(BaseModel):
    url: str
    domain: str
    title: str
    start_time: int
    end_time: int
    duration_sec: int
    category: str
    referrer: str | None = None

