import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any

app = FastAPI(title="DispatchFlow API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

FLEET_FILE = os.path.join(os.path.dirname(__file__), "../data/fleet.json")

def load_fleet():
    if not os.path.exists(FLEET_FILE):
        return {"technicians": [], "jobs": []}
    with open(FLEET_FILE, "r") as f:
        return json.load(f)

@app.get("/api/fleet")
async def get_fleet():
    return load_fleet()

@app.post("/api/dispatch/{tech_id}/{job_id}")
async def dispatch_job(tech_id: int, job_id: int):
    data = load_fleet()
    tech = next((t for t in data["technicians"] if t["id"] == tech_id), None)
    job = next((j for j in data["jobs"] if j["id"] == job_id), None)

    if not tech or not job:
        raise HTTPException(status_code=404, detail="Tech or Job not found")

    tech["status"] = "En Route"
    # Logic simulation: tech "moves" towards job
    return {"status": "success", "message": f"Dispatched {tech['name']} to {job['title']}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
