from fastapi import FastAPI
import uvicorn
from session_manager import load_active_session


from db import init_db
from api import router
from config import PORT

app = FastAPI()
app.include_router(router)

if __name__ == "__main__":
    init_db()
    load_active_session()
    uvicorn.run(app, host="0.0.0.0", port=PORT)
