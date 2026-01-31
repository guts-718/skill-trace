# SkillTrace

SkillTrace is a **local first coding activity tracker** that helps
students and developers understand:

-   Where their time actually goes
-   How much time they spend coding
-   How browsing activity translates into learning

No cloud. No accounts. No tracking servers. Everything runs locally in your system

------------------------------------------------------------------------

## Why SkillTrace?

Most productivity tools:

-   Are cloud based
-   Are generic time trackers
-   Do not understand coding context

SkillTrace is different:

-   Local first
-   Developer focused
-   Built for visibility first, intelligence later

------------------------------------------------------------------------

## Current Status

Phase 1 implemented 

-   Browser activity capture
-   Session merging
-   Local SQLite storage
-   Simple dashboard

Future phases will add classification, coding analytics, and
recommendations.

------------------------------------------------------------------------

## Architecture (Phase 1)

Browser Extension\
→ Local FastAPI Backend\
→ SQLite Database\
→ React Dashboard

------------------------------------------------------------------------

## Features (Phase 1)

-   Track active browser tabs
-   Merge consecutive identical pages into sessions
-   Store sessions locally
-   View today's activity in a web dashboard
-   See total time spent

------------------------------------------------------------------------

## Tech Stack

Backend: - Python - FastAPI - SQLite

Frontend: - React (Vite)

Browser Extension: - Chrome MV3

------------------------------------------------------------------------

## Folder Structure

skill-trace/ ├─ backend/ ├─ frontend/ ├─ extension/

------------------------------------------------------------------------

## Setup Instructions

### 1. Backend

Open terminal:

    cd backend
    python -m venv skillenv
    skillenv\Scripts\activate   (Windows)
    source skillenv/bin/activate  (Mac/Linux)

    pip install fastapi uvicorn pydantic
    python main.py

Backend runs at:

http://localhost:8000

Test:

http://localhost:8000/health

------------------------------------------------------------------------

### 2. Frontend

    cd frontend
    npm install
    npm run dev

Open:

http://localhost:5173

------------------------------------------------------------------------

### 3. Load Browser Extension

Open Chrome:

    chrome://extensions

Enable Developer Mode\
Click Load Unpacked\
Select:

    skill-trace/extension

------------------------------------------------------------------------

## How It Works

1.  Extension sends browsing events
2.  Backend merges events into sessions
3.  Sessions stored in SQLite
4.  Frontend fetches and displays today's sessions

------------------------------------------------------------------------

## Example Session Record

    Google.com
    Start: 10:00
    End:   10:10
    Duration: 600 seconds

------------------------------------------------------------------------

## Privacy

-   No cloud
-   No accounts
-   No external logging
-   All data stored locally

You own your data.

------------------------------------------------------------------------

## Roadmap

Phase 2: - Rule-based classification - Daily reports - Category totals

Phase 3: - LeetCode ingestion - Topic analytics - Suggestions

Phase 4: - Optional LLM - ML-based insights later

------------------------------------------------------------------------

## Disclaimer

SkillTrace is a personal project in early stage of development so expect rough edges.

------------------------------------------------------------------------

## License

MIT
