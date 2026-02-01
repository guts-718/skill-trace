from dotenv import load_dotenv
load_dotenv()
from fastapi import FastAPI
import uvicorn
from scheduler import scheduler_loop
import threading
from telegram_listener import telegram_listener_loop


from db import init_db
from api import router
from config import PORT
from session_manager import load_active_session
from classifier import load_rules

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*","http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

if __name__ == "__main__":
    init_db()
    load_active_session()
    load_rules()
    t = threading.Thread(target=scheduler_loop, daemon=True)
    t.start()
    t2 = threading.Thread(target=telegram_listener_loop, daemon=True)
    t2.start()
    uvicorn.run(app, host="0.0.0.0", port=PORT)
