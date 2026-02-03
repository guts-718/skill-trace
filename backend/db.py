import sqlite3
from config import DB_PATH
from models import Session
import time

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
        duration_sec INTEGER NOT NULL,
        category TEXT NOT NULL,
        user_category TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_settings (
        id INTEGER PRIMARY KEY,
        report_time TEXT,
        email TEXT,
        telegram_chat_id TEXT,
        enable_email INTEGER,
        enable_telegram INTEGER,
        last_sent_date TEXT,
        leetcode_username,
        last_leetcode_sync
    )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leetcode_submissions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        problem_id INTEGER,
        title TEXT,
        title_slug TEXT,
        difficulty TEXT,
        tags TEXT,
        solved_at INTEGER,
        UNIQUE(problem_id, solved_at)
    )

    """)

    cursor.execute("""
    INSERT OR IGNORE INTO user_settings
    (id, report_time, email, telegram_chat_id, enable_email, enable_telegram, last_sent_date, leetcode_username)
    VALUES (1, "21:00", "", "", 0, 0, "", "")

    """)

    # SQLite does not support IF NOT EXISTS for ADD COLUMN.
    try:
        cursor.execute("""
        ALTER TABLE user_settings
        ADD COLUMN leetcode_username TEXT
        """)
    except:
        pass

    try:
        cursor.execute("""
        ALTER TABLE user_settings
        ADD COLUMN last_leetcode_sync INTEGER
        """)
    except:
        pass


    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leetcode_problems (
        problem_id INTEGER PRIMARY KEY,
        title_slug TEXT UNIQUE,
        title TEXT,
        difficulty TEXT,
        tags TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS leetcode_skill_snapshots (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        snapshot_json TEXT,
        fetched_at INTEGER
    )
    """)

    try:
        cursor.execute("""
        ALTER TABLE user_settings
        ADD COLUMN last_skill_snapshot_date TEXT
        """)
    except:
        pass

    conn.commit()
    conn.close()



def update_last_skill_snapshot_date(date_str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE user_settings
        SET last_skill_snapshot_date=?
        WHERE id=1
    """, (date_str,))
    conn.commit()
    conn.close()

def insert_session(session: Session):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO web_sessions
        (url, domain, title, start_time, end_time, duration_sec, category)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        session.url,
        session.domain,
        session.title,
        session.start_time,
        session.end_time,
        session.duration_sec,
        session.category
    ))


    conn.commit()
    conn.close()


def get_sessions_between(start_ts: int, end_ts: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
     SELECT id, url, domain, title, start_time, end_time, duration_sec, category, user_category
     FROM web_sessions
        WHERE start_time >= ? AND start_time <= ?
        ORDER BY start_time ASC
    """, (start_ts, end_ts))

    rows = cursor.fetchall()
    conn.close()

    sessions = []
    for r in rows:
        sessions.append({
            "id": r[0],
            "url": r[1],
            "domain": r[2],
            "title": r[3],
            "start_time": r[4],
            "end_time": r[5],
            "duration_sec": r[6],
            "category": r[7],
            "user_category": r[8]
        })




    return sessions


def update_user_category(session_id: int, category: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE web_sessions
        SET user_category = ?
        WHERE id = ?
    """, (category, session_id))

    conn.commit()
    conn.close()

def get_total_time_between(start_ts: int, end_ts: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT SUM(duration_sec)
        FROM web_sessions
        WHERE start_time >= ? AND start_time <= ?
    """, (start_ts, end_ts))

    val = cur.fetchone()[0]
    conn.close()
    return val or 0


def get_category_breakdown(start_ts: int, end_ts: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
          COALESCE(user_category, category) as cat,
          SUM(duration_sec)
        FROM web_sessions
        WHERE start_time >= ? AND start_time <= ?
        GROUP BY cat
    """, (start_ts, end_ts))

    rows = cur.fetchall()
    conn.close()

    return {r[0]: r[1] for r in rows}


def get_top_domains(start_ts: int, end_ts: int, limit=5):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT domain, SUM(duration_sec) as t
        FROM web_sessions
        WHERE start_time >= ? AND start_time <= ?
        GROUP BY domain
        ORDER BY t DESC
        LIMIT ?
    """, (start_ts, end_ts, limit))

    rows = cur.fetchall()
    conn.close()

    return [{"domain": r[0], "time": r[1]} for r in rows]


def get_session_count(start_ts: int, end_ts: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*)
        FROM web_sessions
        WHERE start_time >= ? AND start_time <= ?
    """, (start_ts, end_ts))

    val = cur.fetchone()[0]
    conn.close()
    return val

def get_settings():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT report_time, email, telegram_chat_id,enable_email, enable_telegram,leetcode_username, last_leetcode_sync FROM user_settings WHERE id=1")
    row = cur.fetchone()
    conn.close()

    return {
    "report_time": row[0],
    "email": row[1],
    "telegram_chat_id": row[2],
    "enable_email": bool(row[3]),
    "enable_telegram": bool(row[4]),
    "leetcode_username": row[5],
    "last_leetcode_sync": row[6]
    }



def save_settings(s):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE user_settings
        SET report_time=?,
        email=?,
        telegram_chat_id=?,
        enable_email=?,
        enable_telegram=?,
        leetcode_username=?,
        last_sent_date=""
        WHERE id=1
    """, (
        s["report_time"],
        s["email"],
        s["telegram_chat_id"],
        int(s["enable_email"]),
        int(s["enable_telegram"]),
        s.get("leetcode_username","")
    ))

    conn.commit()
    conn.close()


def get_last_sent_date():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT last_sent_date FROM user_settings WHERE id=1")
    val = cur.fetchone()[0]
    conn.close()
    return val or ""


def update_last_sent_date(date_str: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE user_settings
        SET last_sent_date = ?
        WHERE id=1
    """, (date_str,))

    conn.commit()
    conn.close()


def insert_leetcode_submission(problem_id, title, title_slug, difficulty, tags, solved_at):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT OR IGNORE INTO leetcode_submissions
        (problem_id, title, title_slug, difficulty, tags, solved_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        problem_id,
        title,
        title_slug,
        difficulty,
        ",".join(tags),
        solved_at
    ))

    print("Attempt insert:", problem_id, solved_at)
    inserted = cur.rowcount
    print("Rowcount:", inserted)

    # inserted = cur.rowcount  # 1 if inserted, 0 if ignored
    conn.commit()
    conn.close()

    return inserted


def get_cached_problem(title_slug):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT problem_id, title, title_slug, difficulty, tags
        FROM leetcode_problems
        WHERE title_slug = ?
    """, (title_slug,))

    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "problem_id": row[0],
        "title": row[1],
        "title_slug": row[2],
        "difficulty": row[3],
        "tags": row[4].split(",") if row[4] else []
    }


def cache_problem(problem):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT OR IGNORE INTO leetcode_problems
        (problem_id, title_slug, title, difficulty, tags)
        VALUES (?, ?, ?, ?, ?)
    """, (
        problem["problem_id"],
        problem["title_slug"],
        problem["title"],
        problem["difficulty"],
        ",".join(problem["tags"])
    ))

    conn.commit()
    conn.close()

def update_last_leetcode_sync(ts: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        UPDATE user_settings
        SET last_leetcode_sync=?
        WHERE id=1
    """, (ts,))

    conn.commit()
    conn.close()


## LC analytics

def get_leetcode_total_solved():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(DISTINCT problem_id) FROM leetcode_submissions")
    val = cur.fetchone()[0]
    conn.close()
    return val or 0


def get_leetcode_difficulty_counts():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT difficulty, COUNT(*)
        FROM leetcode_submissions
        GROUP BY difficulty
    """)

    rows = cur.fetchall()
    conn.close()

    return {r[0]: r[1] for r in rows}


def get_leetcode_recent(limit=10):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT title, difficulty, solved_at
        FROM leetcode_submissions
        ORDER BY solved_at DESC
        LIMIT ?
    """, (limit,))

    rows = cur.fetchall()
    conn.close()

    return [
        {"title": r[0], "difficulty": r[1], "timestamp": r[2]}
        for r in rows
    ]


def get_topic_last_seen():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT tags, MAX(solved_at)
        FROM leetcode_submissions
        GROUP BY tags
    """)

    rows = cur.fetchall()
    conn.close()

    topic_map = {}

    for tags_str, ts in rows:
        if not tags_str:
            continue
        tags = tags_str.split(",")
        for t in tags:
            if t not in topic_map or ts > topic_map[t]:
                topic_map[t] = ts

    return topic_map


def insert_skill_snapshot(snapshot_json, ts):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO leetcode_skill_snapshots (snapshot_json, fetched_at)
        VALUES (?, ?)
    """, (snapshot_json, ts))

    conn.commit()
    conn.close()


def get_latest_skill_snapshot():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT snapshot_json
        FROM leetcode_skill_snapshots
        ORDER BY fetched_at DESC
        LIMIT 1
    """)

    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    import json
    return json.loads(row[0])


# topic freq last n dats

def get_topic_frequency(days: int):
    conn = get_connection()
    cur = conn.cursor()

    cutoff = int(time.time()) - days * 86400

    cur.execute("""
        SELECT tags
        FROM leetcode_submissions
        WHERE solved_at >= ?
    """, (cutoff,))

    rows = cur.fetchall()
    conn.close()

    freq = {}

    for (tags_str,) in rows:
        if not tags_str:
            continue
        for t in tags_str.split(","):
            freq[t] = freq.get(t, 0) + 1

    return freq


def get_total_solved_per_topic():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT tags, COUNT(*)
        FROM leetcode_submissions
        GROUP BY tags
    """)

    rows = cur.fetchall()
    conn.close()

    totals = {}

    for tags_str, cnt in rows:
        if not tags_str:
            continue
        for t in tags_str.split(","):
            totals[t] = totals.get(t, 0) + cnt

    return totals
