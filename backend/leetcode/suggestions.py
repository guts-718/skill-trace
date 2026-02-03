import math
import time

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

        priorities[t] = score

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
    ordered = sorted(priorities.items(),
                     key=lambda x: x[1],
                     reverse=True)

    difficulty = decide_difficulty()

    result = []
    for topic, score in ordered[:k]:
        result.append({
            "topic": topic,
            "priority": round(score, 3),
            "difficulty": difficulty
        })

    return result
