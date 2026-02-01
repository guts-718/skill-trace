import json
import os
from models import Session
from config import ACTIVE_SESSION_FILE
from db import insert_session
from classifier import classify_session

last_session = None

def load_active_session():
    global last_session

    if not os.path.exists(ACTIVE_SESSION_FILE):
        return

    try:
        with open(ACTIVE_SESSION_FILE, "r") as f:
            data = json.load(f)
            last_session = Session(**data)
    except Exception:
        # corrupted or empty file → ignore
        last_session = None


def persist_active_session():
    if last_session is None:
        return
    with open(ACTIVE_SESSION_FILE, "w") as f:
        json.dump(last_session.model_dump(), f)

def finalize_last_session():
    global last_session

    if last_session is None:
        return

    last_session.duration_sec = (
        last_session.end_time - last_session.start_time
    )

    # drop very short sessions (noise)
    if last_session.duration_sec < 5: # need to make it 45. but for dev for now it is 5
        last_session = None
        if os.path.exists(ACTIVE_SESSION_FILE):
            os.remove(ACTIVE_SESSION_FILE)
        return


    # classify
    category = classify_session(last_session)
    last_session.category = category

    insert_session(last_session)

    # delete persisted active session file
    if os.path.exists(ACTIVE_SESSION_FILE):
        os.remove(ACTIVE_SESSION_FILE)

    last_session = None



def process_event(event):
    print("EVENT:", event.url)
    global last_session
    if last_session:
        print("LAST SESSION URL:", last_session.url)

    

    if last_session is None:
        last_session = Session(
            url=event.url,
            domain=event.domain,
            title=event.title,
            start_time=event.timestamp,
            end_time=event.timestamp,
            duration_sec=0,
            category="Other",
            referrer=event.referrer
        )
        persist_active_session()
        return

    if event.url == last_session.url:
        last_session.end_time = event.timestamp
        persist_active_session()
        return
    print("FINALIZING SESSION:", last_session.url)
    finalize_last_session()

    last_session = Session(
        url=event.url,
        domain=event.domain,
        title=event.title,
        start_time=event.timestamp,
        end_time=event.timestamp,
        duration_sec=0,
        category="Other",
        referrer=event.referrer
    )
    persist_active_session()
