from fastapi import FastAPI
import uvicorn

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
    uvicorn.run(app, host="0.0.0.0", port=PORT)
