FETCH_LIMIT = 20
SLEEP_BETWEEN_REQUESTS = 0.4 # This need refinement.
MAX_WORKERS = 4
USERNAME="ratneshk01"
leetcode_sync_lock = False


import os
import time
from db import get_cached_problem, cache_problem
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from db import update_last_leetcode_sync, get_settings
from leetcode.client import fetch_leetcode_skill
from db import insert_skill_snapshot,  update_last_skill_snapshot_date
import json




from leetcode.client import (
    fetch_recent_submissions,
    fetch_problem_details
)

from db import insert_leetcode_submission


def delete_db():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, "skilltrace.db")

    if os.path.exists(db_path):
        os.remove(db_path)
        print("Deleted skilltrace.db")
    else:
        print("skilltrace.db not found")


def sync_leetcode_sequential(username: str):
    global leetcode_sync_lock
    if leetcode_sync_lock:
        print("LeetCode sync already running")
        return 0

    leetcode_sync_lock = True
    submissions = fetch_recent_submissions(username, limit=FETCH_LIMIT)
    new_count = 0

    start = time.perf_counter()

    for sub in submissions:
        slug = sub["title_slug"]
        ts = sub["timestamp"]

        details = get_cached_problem(slug)
        if not details:
            details = fetch_problem_details(slug)
            if not details:
                continue
            cache_problem(details)

        inserted = insert_leetcode_submission(
            details["problem_id"],
            details["title"],
            details["title_slug"],
            details["difficulty"],
            details["tags"],
            ts
        )

        if inserted:
            new_count += 1

    update_last_leetcode_sync(int(time.time()))
    leetcode_sync_lock = False
    end = time.perf_counter()
    return new_count, end - start



def sync_leetcode_concurrent(username: str):
    global leetcode_sync_lock
    if leetcode_sync_lock:
        print("LeetCode sync already running")
        return 0

    leetcode_sync_lock = True

    submissions = fetch_recent_submissions(username, limit=FETCH_LIMIT)
    new_count = 0
    to_fetch = []

    start = time.perf_counter()

    for sub in submissions:
        slug = sub["title_slug"]
        ts = sub["timestamp"]

        details = get_cached_problem(slug)
        if details:
            inserted = insert_leetcode_submission(
                details["problem_id"],
                details["title"],
                details["title_slug"],
                details["difficulty"],
                details["tags"],
                ts
            )
            if inserted:
                new_count += 1
        else:
            to_fetch.append((slug, ts))

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(fetch_problem_details, slug): (slug, ts)
            for slug, ts in to_fetch
        }

        for future in as_completed(futures):
            slug, ts = futures[future]
            try:
                details = future.result()
                if not details:
                    continue

                cache_problem(details)

                inserted = insert_leetcode_submission(
                    details["problem_id"],
                    details["title"],
                    details["title_slug"],
                    details["difficulty"],
                    details["tags"],
                    ts
                )

                if inserted:
                    new_count += 1

            except Exception as e:
                leetcode_sync_lock = False
                print("Error:", e)

    update_last_leetcode_sync(int(time.time()))
    leetcode_sync_lock = False

    maybe_store_skill_snapshot(username)
    end = time.perf_counter()

    return new_count, end - start


def maybe_sync_leetcode(username: str, min_gap_sec: int):
    settings = get_settings()
    last = settings.get("last_leetcode_sync") or 0
    now = int(time.time())

    if now - last < min_gap_sec:
        print("LeetCode sync skipped (recent)")
        return 0

    # return sync_leetcode_sequential(username)
    return sync_leetcode_concurrent(username)



def maybe_store_skill_snapshot(username: str):
    today = time.strftime("%Y-%m-%d")

    # reuse user_settings.last_sent_date style logic
    settings = get_settings()
    last = settings.get("last_skill_snapshot_date", "")

    if last == today:
        return

    skill = fetch_leetcode_skill(username)
    insert_skill_snapshot(json.dumps(skill), int(time.time()))

    # reuse same table, add another column if needed later
    update_last_skill_snapshot_date(today)


# -------------------------
# Manual Test
# -------------------------
if __name__ == "__main__":
    user = USERNAME
    # delete_db()
    # print("Running sequential...")
    # n1, t1 = sync_leetcode_sequential(user)
    # print(f"Sequential: {t1:.2f}s, new records: {n1}")
    # delete_db()
    print("Running concurrent...")
    n2, t2 = sync_leetcode_concurrent(user)
    print(f"Concurrent: {t2:.2f}s, new records: {n2}")
