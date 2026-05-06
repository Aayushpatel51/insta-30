import os
import json
from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

app = FastAPI(title="AdminFlow - Low-Code Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_FILE = os.path.join(os.path.dirname(__file__), "../data/database.json")

def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.get("/api/schema")
async def get_schema():
    """Returns available tables and their field names (based on first record)."""
    db = load_db()
    schema = {}
    for table, records in db.items():
        fields = list(records[0].keys()) if records else []
        schema[table] = {
            "count": len(records),
            "fields": fields
        }
    return schema

@app.get("/api/resources/{table}")
async def get_resources(table: str):
    db = load_db()
    if table not in db:
        raise HTTPException(status_code=404, detail="Table not found")
    return db[table]

@app.post("/api/resources/{table}")
async def create_resource(table: str, data: Dict[str, Any] = Body(...)):
    db = load_db()
    if table not in db:
        db[table] = []

    # Simple ID generation
    new_id = max([r.get("id", 0) for r in db[table]], default=0) + 1
    data["id"] = new_id
    db[table].append(data)
    save_db(db)
    return data

@app.put("/api/resources/{table}/{item_id}")
async def update_resource(table: str, item_id: int, data: Dict[str, Any] = Body(...)):
    db = load_db()
    if table not in db:
        raise HTTPException(status_code=404, detail="Table not found")

    for i, item in enumerate(db[table]):
        if item.get("id") == item_id:
            db[table][i].update(data)
            db[table][i]["id"] = item_id # Ensure ID doesn't change
            save_db(db)
            return db[table][i]

    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/api/resources/{table}/{item_id}")
async def delete_resource(table: str, item_id: int):
    db = load_db()
    if table not in db:
        raise HTTPException(status_code=404, detail="Table not found")

    db[table] = [item for item in db[table] if item.get("id") != item_id]
    save_db(db)
    return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
