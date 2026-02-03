import requests
import time

BASE_URL = "https://alfa-leetcode-api.onrender.com"


# -----------------------------
# Fetch Recent Accepted Submissions
# -----------------------------

def fetch_recent_submissions(username: str, limit: int = 20, offset: int = 0):
    url = f"{BASE_URL}/{username}/acSubmission"
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()

    data = resp.json()
    subs = data.get("submission", [])

    result = []
    for s in subs[:limit]:
        result.append({
            "title": s["title"],
            "title_slug": s["titleSlug"],
            "timestamp": int(s["timestamp"])
        })

    return result



# -----------------------------
# Fetch Problem Metadata
# -----------------------------

def fetch_problem_details(title_slug: str):
    url = f"{BASE_URL}/select?titleSlug={title_slug}"
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()

    data = resp.json()

    return {
        "problem_id": int(data["questionId"]),
        "title": data["questionTitle"],
        "title_slug": title_slug,
        "difficulty": data["difficulty"],
        "tags": [t["name"] for t in data.get("topicTags", [])]
    }


def fetch_leetcode_calendar(username: str, year: int):
    url = f"{BASE_URL}/{username}/calendar?year={year}"
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    return resp.json()

def fetch_leetcode_skill(username: str):
    url = f"{BASE_URL}/{username}/skill"
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    return resp.json()


# -----------------------------
# Manual Test
# -----------------------------

if __name__ == "__main__":
    subs = fetch_recent_submissions("ratneshk01",5, 0)
    print(subs)

    if subs:
        details = fetch_problem_details(subs[0]["title_slug"])
        print(details)

