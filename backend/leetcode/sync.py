FETCH_LIMIT = 20
SLEEP_BETWEEN_REQUESTS = 0.4 # This need refinement.
USERNAME="ratneshk01"
import time
from db import get_cached_problem, cache_problem

from leetcode.client import (
    fetch_recent_submissions,
    fetch_problem_details
)

from db import insert_leetcode_submission





def sync_leetcode(username: str):
    print(f"Starting LeetCode sync for {username}")

    submissions = fetch_recent_submissions(username, limit=FETCH_LIMIT)

    new_count = 0

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

        time.sleep(SLEEP_BETWEEN_REQUESTS)

    print(f"LeetCode sync done. New records: {new_count}")
    return new_count


# -------------------------
# Manual Test
# -------------------------

if __name__ == "__main__":
    sync_leetcode(USERNAME)
