import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"   # chose whichever

def explain(signals: dict):
    prompt = f"""
You are a blunt but caring coding mentor.

Topic: {signals['topic']}
Signals:
- Days since last practice: {signals['days_since_last']}
- Total problems solved: {signals['total_solved']}
- Solved in last week: {signals['recent_7d']}

Write 1–2 short lines (max 50 words).
Tone: sometimes teasing friend, sometimes older sibling, sometimes funny.
It should lightly sting but be supportive.
Call out inconsistency or fake effort when applicable.
No emojis. No fluff.
"""


    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    }

    try:
        res = requests.post(OLLAMA_URL, json=payload, timeout=20)
        text = res.json()["response"]
        return [text.strip()]
    except Exception:
        return None
