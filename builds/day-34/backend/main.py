from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os

app = FastAPI(title="Shadow IT Discovery API")

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class OAuthApp(BaseModel):
    id: str
    name: str
    category: str
    risk_level: str  # High, Medium, Low
    users_affected: int
    scopes: List[str]
    icon: str
    discovered_at: str
    status: str  # Active, Revoked, Under Review

# Simulated Shadow IT Data
APPS_DB = [
    {
        "id": "app_1",
        "name": "PDF Swift Converter",
        "category": "Utility",
        "risk_level": "High",
        "users_affected": 12,
        "scopes": ["mail.read", "files.read.all", "profile"],
        "icon": "📄",
        "discovered_at": "2023-10-24 14:20",
        "status": "Active"
    },
    {
        "id": "app_2",
        "name": "QuickCalendar Sync",
        "category": "Productivity",
        "risk_level": "Medium",
        "users_affected": 45,
        "scopes": ["calendar.read", "profile"],
        "icon": "📅",
        "discovered_at": "2023-10-25 09:15",
        "status": "Active"
    },
    {
        "id": "app_3",
        "name": "Emoji Keyboard Pro",
        "category": "Entertainment",
        "risk_level": "High",
        "users_affected": 5,
        "scopes": ["contacts.read", "profile", "mail.send"],
        "icon": "🎨",
        "discovered_at": "2023-10-26 18:30",
        "status": "Active"
    },
    {
        "id": "app_4",
        "name": "Zoom Backgrounds Plus",
        "category": "Social",
        "risk_level": "Low",
        "users_affected": 120,
        "scopes": ["profile"],
        "icon": "🖼️",
        "discovered_at": "2023-10-27 11:00",
        "status": "Active"
    },
    {
        "id": "app_5",
        "name": "Notes AI Summarizer",
        "category": "AI Tools",
        "risk_level": "Medium",
        "users_affected": 28,
        "scopes": ["files.read", "profile"],
        "icon": "🤖",
        "discovered_at": "2023-10-27 15:45",
        "status": "Active"
    }
]

@app.get("/api/apps", response_model=List[OAuthApp])
async def get_apps():
    return APPS_DB

@app.post("/api/revoke/{app_id}")
async def revoke_app(app_id: str):
    for app in APPS_DB:
        if app["id"] == app_id:
            app["status"] = "Revoked"
            return {"message": f"Access revoked for {app['name']}", "app_id": app_id}
    raise HTTPException(status_code=404, detail="App not found")

@app.get("/api/stats")
async def get_stats():
    high_risk = len([a for a in APPS_DB if a["risk_level"] == "High"])
    total_users = sum([a["users_affected"] for a in APPS_DB])
    return {
        "total_apps": len(APPS_DB),
        "high_risk_count": high_risk,
        "total_exposed_users": total_users,
        "critical_alerts": high_risk
    }

# Mount frontend
frontend_path = os.path.join(os.path.dirname(__file__), "../frontend")
if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
