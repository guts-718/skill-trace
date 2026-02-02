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
        leetcode_username
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

    cur.execute("SELECT report_time, email, telegram_chat_id, enable_email, enable_telegram, leetcode_username FROM user_settings WHERE id=1")
    row = cur.fetchone()
    conn.close()

    return {
    "report_time": row[0],
    "email": row[1],
    "telegram_chat_id": row[2],
    "enable_email": bool(row[3]),
    "enable_telegram": bool(row[4]),
    "leetcode_username": row[5]
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
