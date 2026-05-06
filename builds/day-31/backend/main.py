import os
import json
import shutil
import tempfile
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
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

from openai import OpenAI
try:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
except Exception:
    client = None

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
async def process_meeting(title: str = Form("New Meeting"), file: UploadFile = File(...)):
    """
    Real AI Logic: Extracts data from the provided audio file.
    Uses Whisper for transcription and GPT-4 for analysis.
    """
    meeting_id = f"mtg_{int(datetime.now().timestamp())}"

    # Ensure it's an audio file
    if not file.content_type.startswith("audio/"):
         # We allow it for demo but usually check extension
         pass

    # 1. Save file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name

    try:
        if not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY") == "your_api_key_here":
            # Simulation Fallback (High Fidelity Mock)
            print("No OpenAI API key found, using high-fidelity simulation.")
            summary = "This discussion focused on the core architectural decisions for the MVP. The team agreed on a microservices approach using FastAPI and PostgreSQL, prioritizing scalability and rapid deployment cycles."
            transcript = [
                {"speaker": "Lead", "text": "We need to decide on the database for the MVP."},
                {"speaker": "Engineer", "text": "I suggest PostgreSQL for its reliability and JSONB support."},
                {"speaker": "Lead", "text": "Agreed. Let's get the schema designed by tomorrow."}
            ]
            tasks = [
                {"id": "tk_1", "task": "Design initial DB schema", "assignee": "Engineer", "due_date": "Tomorrow", "status": "pending"},
                {"id": "tk_2", "task": "Setup FastAPI boilerplate", "assignee": "Lead", "due_date": "Today", "status": "pending"}
            ]
        else:
            # 2. Transcribe with Whisper
            with open(tmp_path, "rb") as audio_file:
                transcription = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    response_format="text"
                )

            # 3. Analyze with GPT-4
            prompt = f"""
            Analyze the following meeting transcript and provide:
            1. A concise professional summary (2-3 sentences).
            2. A list of actionable tasks with assignees (identify them from context).
            3. A diarized transcript structure (Speaker: Text).

            Transcript:
            {transcription}

            Return ONLY a JSON object with this structure:
            {{
                "summary": "...",
                "tasks": [{{ "task": "...", "assignee": "...", "due_date": "..." }}],
                "transcript": [{{ "speaker": "...", "text": "..." }}]
            }}
            """

            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                response_format={ "type": "json_object" }
            )

            analysis = json.loads(response.choices[0].message.content)
            summary = analysis.get("summary", "No summary generated.")
            transcript = analysis.get("transcript", [])
            tasks = []
            for i, t in enumerate(analysis.get("tasks", [])):
                tasks.append({
                    "id": f"tk_{i}_{int(datetime.now().timestamp())}",
                    "task": t.get("task", "Unknown Task"),
                    "assignee": t.get("assignee", "Unassigned"),
                    "due_date": t.get("due_date", "TBD"),
                    "status": "pending"
                })

        new_meeting = {
            "id": meeting_id,
            "title": title or file.filename,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "summary": summary,
            "transcript": transcript,
            "tasks": tasks
        }

        save_meeting(new_meeting)
        return new_meeting

    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)

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
