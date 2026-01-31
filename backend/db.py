import sqlite3
from config import DB_PATH
from models import Session


def get_connection():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS web_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT NOT NULL,
        domain TEXT NOT NULL,
        title TEXT NOT NULL,
        start_time INTEGER NOT NULL,
        end_time INTEGER NOT NULL,
        duration_sec INTEGER NOT NULL
    )
    """)

    conn.commit()
    conn.close()


def insert_session(session: Session):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO web_sessions
        (url, domain, title, start_time, end_time, duration_sec)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        session.url,
        session.domain,
        session.title,
        session.start_time,
        session.end_time,
        session.duration_sec
    ))

    conn.commit()
    conn.close()


def get_sessions_between(start_ts: int, end_ts: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT url, domain, title, start_time, end_time, duration_sec
        FROM web_sessions
        WHERE start_time >= ? AND start_time <= ?
        ORDER BY start_time ASC
    """, (start_ts, end_ts))

    rows = cursor.fetchall()
    conn.close()

    sessions = []
    for r in rows:
        sessions.append({
            "url": r[0],
            "domain": r[1],
            "title": r[2],
            "start_time": r[3],
            "end_time": r[4],
            "duration_sec": r[5]
        })

    return sessions
