import os
import json
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# --- SaaS Models ---
class Task(BaseModel):
    id: str
    task: str
    assignee: str
    due_date: str
    status: str = "pending"

class MeetingDetail(BaseModel):
    id: str
    title: str
    date: str
    summary: str
    transcript: List[dict]
    tasks: List[Task]

# --- App Initialization ---
app = FastAPI(title="MeetingFlow SaaS API")

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock DB (In a real SaaS, this would be PostgreSQL)
# Using relative pathing from the app root
MOCK_DB_PATH = os.path.join(os.path.dirname(__file__), "../data/meetings.json")

def get_meetings():
    if not os.path.exists(MOCK_DB_PATH):
        return []
    with open(MOCK_DB_PATH, "r") as f:
        return json.load(f)

def save_meeting(meeting: dict):
    meetings = get_meetings()
    meetings.append(meeting)
    os.makedirs(os.path.dirname(MOCK_DB_PATH), exist_ok=True)
    with open(MOCK_DB_PATH, "w") as f:
        json.dump(meetings, f, indent=4)

# --- Endpoints ---

@app.get("/api/meetings")
async def list_meetings():
    return get_meetings()

@app.post("/api/process-meeting")
async def process_meeting(title: str = "New Meeting"):
    """
    SaaS Logic: Simulates the AI pipeline for a new meeting upload.
    """
    meeting_id = f"mtg_{int(datetime.now().timestamp())}"

    # Mock AI Processing Result
    new_meeting = {
        "id": meeting_id,
        "title": title,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "summary": "This is an AI-generated summary of your recent discussion regarding the MVP launch roadmap and database architecture.",
        "transcript": [
            {"speaker": "Founder", "text": "We need to launch by the end of the month."},
            {"speaker": "Senior Dev", "text": "The API is ready, we just need the migration scripts."},
            {"speaker": "Founder", "text": "Great, let's prioritize that."}
        ],
        "tasks": [
            {"id": "tk_1", "task": "Write migration scripts", "assignee": "Senior Dev", "due_date": "Today", "status": "pending"},
            {"id": "tk_2", "task": "Finalize launch checklist", "assignee": "Founder", "due_date": "Friday", "status": "pending"}
        ]
    }

    save_meeting(new_meeting)
    return new_meeting

@app.post("/api/sync-notion/{meeting_id}")
async def sync_notion(meeting_id: str):
    """
    SaaS Integration Logic: Simulates syncing to Notion.
    """
    meetings = get_meetings()
    meeting = next((m for m in meetings if m["id"] == meeting_id), None)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")

    # Simulate real integration logic
    return {"status": "success", "message": f"Successfully synced {len(meeting['tasks'])} tasks to Notion."}

# Serve the static frontend
frontend_dir = os.path.join(os.path.dirname(__file__), "../frontend")
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
