import math
import time
from leetcode.client import fetch_problems
from db import get_all_solved_problem_ids
import random


from db import (
    get_topic_last_seen,
    get_total_solved_per_topic,
    get_topic_frequency,
    get_leetcode_difficulty_counts
)

# ---------- Scoring helpers ----------

def recency_score(days):
    return min(days / 30.0, 2.0)

def weakness_score(total):
    return 1 / math.sqrt(total + 1)

def momentum_penalty(recent):
    return min(recent / 5.0, 1.0)

# ---------- Main Engine ----------

def compute_topic_priorities():
    now = int(time.time())

    last_seen = get_topic_last_seen()
    totals = get_total_solved_per_topic()
    recent7 = get_topic_frequency(7)

    topics = set()
    topics.update(last_seen.keys())
    topics.update(totals.keys())

    priorities = {}

    for t in topics:
        days_since = (
            (now - last_seen[t]) / 86400
            if t in last_seen else 999
        )

        total = totals.get(t, 0)
        recent = recent7.get(t, 0)

        score = (
            1.2 * recency_score(days_since)
            + 1.0 * weakness_score(total)
            - 0.8 * momentum_penalty(recent)
        )

        if total == 0:
            score += 2

        if total > 200:
            score *= 0.4

        priorities[t] = {
            "score": score,
            "days_since": days_since,
            "total": total,
            "recent": recent
        }


    return priorities


def decide_difficulty():
    dist = get_leetcode_difficulty_counts()

    hard = dist.get("Hard", 0)
    medium = dist.get("Medium", 0)

    if hard == 0:
        return "Hard"

    if medium < 3:
        return "Medium"

    return "Medium"


def generate_topic_suggestions(k=3):
    priorities = compute_topic_priorities()
    ordered = sorted(
        priorities.items(),
        key=lambda x: x[1]["score"],
        reverse=True
    )


    difficulty = decide_difficulty()

    result = []
    for topic, data in ordered[:k]:
        result.append({
            "topic": topic,
            "priority": data["score"],
            "difficulty": difficulty,
            "signals": data
        })


    return result

def generate_suggestions():
    topics = generate_topic_suggestions()
    final = []

    for item in topics:
        probs = select_problems_for_topic(
            item["topic"],
            item["difficulty"],
            k=2
        )

        if not probs:
            continue

        final.append({
            "topic": item["topic"],
            "priority": item["priority"],
            "reason": build_explanation(item["topic"], item["signals"]),
            "problems": probs
        })


    return final


# {'acRate': 47.79178582580149, 'difficulty': 'Medium', 'freqBar': None, 'questionFrontendId': '2', 
# 'isFavor': False, 'isPaidOnly': False, 'status': None, 'title': 'Add Two Numbers', 
# 'titleSlug': 'add-two-numbers', 'topicTags': [{'name': 'Linked List', 'id': 'VG9waWNUYWdOb2RlOjc=', '
# 'slug': 'linked-list'}, {'name': 'Math', 'id': 'VG9waWNUYWdOb2RlOjg=', 'slug': 'math'}, 
# {'name': 'Recursion', 'id': 'VG9waWNUYWdOb2RlOjMx', 'slug': 'recursion'}], 'hasSolution': True,
#  'hasVideoSolution': True}


def select_problems_for_topic(topic, difficulty, k=2):
    problems = fetch_problems(topic, difficulty)
    solved_ids = get_all_solved_problem_ids()

    candidates = []
    print("problems: ",problems["problemsetQuestionList"][0])
    for p in problems["problemsetQuestionList"]:
        pid = int(p["questionFrontendId"])
        if pid in solved_ids:
            continue

        candidates.append(p)

    if not candidates:
        return []

    import random
    random.shuffle(candidates)
    chosen = candidates[:k]

    return [
        {
            "problem_id": int(p["questionFrontendId"]),
            "title": p["title"],
            "difficulty": p["difficulty"],
            "link": f"https://leetcode.com/problems/{p['titleSlug']}"
        }
        for p in chosen
    ]

def build_explanation(topic, signals):
    reasons = []

    days = int(signals["days_since"])
    total = signals["total"]
    recent = signals["recent"]

    if total == 0:
        reasons.append("You have never practiced this topic")

    if days > 30:
        reasons.append(f"Not practiced in {days} days")

    if total < 30:
        reasons.append(f"Only {total} problems solved so far")

    if recent == 0:
        reasons.append("No problems solved from this topic in the last week")

    if not reasons:
        reasons.append("Good topic for balanced practice")

    return reasons
