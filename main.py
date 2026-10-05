from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os

app = FastAPI(title="UAE Expat Private Expense Planner", version="1.0")

# Nested database structure: { email: { month: encrypted_payload } }
ENCRYPTED_DB = {}

class SaveDataRequest(BaseModel):
    email: str
    month: str
    encrypted_payload: str

if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return {"message": "Welcome to the UAE Expat Privacy-First Expense Planner API!"}

@app.post("/api/save-expense")
def save_encrypted_data(data: SaveDataRequest):
    if data.email not in ENCRYPTED_DB:
        ENCRYPTED_DB[data.email] = {}
    ENCRYPTED_DB[data.email][data.month] = data.encrypted_payload
    return {"status": "success", "message": f"Data securely saved for {data.month}."}

@app.get("/api/get-expense/{email}/{month}")
def get_encrypted_data(email: str, month: str):
    if email not in ENCRYPTED_DB or month not in ENCRYPTED_DB[email]:
        return {"encrypted_payload": None}
    return {"email": email, "month": month, "encrypted_payload": ENCRYPTED_DB[email][month]}
