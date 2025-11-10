
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import uuid

from .services.jobs import JobStore
from .services.lyrics import generate_lyrics_stub
from .services.compose import compose_stub
from .services.separate import separate_stub
from .services.reintegrate import reintegrate_stub

app = FastAPI(title="AI Music Studio API", version="0.1.0")

# CORS (dev-friendly)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

jobs = JobStore()

class LyricsIn(BaseModel):
    genre: str = "pop"
    mood: str = "joyful"
    length: Dict[str, int] = {"verses": 2, "choruses": 1}
    prompt: Optional[str] = None

@app.post("/v1/lyrics.generate")
async def lyrics_generate(payload: LyricsIn):
    job_id = jobs.create("lyrics.generate")
    result = generate_lyrics_stub(payload.model_dump())
    jobs.complete(job_id, result)
    return {"job_id": job_id, "result": result}

class ComposeIn(BaseModel):
    key: str = "C major"
    tempo_bpm: int = 120
    style: str = "electronic-pop"
    duration_sec: int = 150
    instrumentation: list[str] = ["drums","bass","pads","lead"]

@app.post("/v1/compose.generate")
async def compose_generate(payload: ComposeIn):
    job_id = jobs.create("compose.generate")
    result = compose_stub(payload.model_dump())
    jobs.complete(job_id, result)
    return {"job_id": job_id, "result": result}

@app.post("/v1/separate.vocals")
async def separate_vocals(file: UploadFile = File(...)):
    job_id = jobs.create("separate.vocals")
    result = await separate_stub(file)
    jobs.complete(job_id, result)
    return {"job_id": job_id, "result": result}

@app.post("/v1/mix.reintegrate")
async def mix_reintegrate(
    instrumental: UploadFile = File(...),
    vocals: UploadFile = File(...),
    key: str = Form("C major"),
    tempo_bpm: int = Form(120),
    preset: str = Form("pop-clear"),
):
    job_id = jobs.create("mix.reintegrate")
    result = await reintegrate_stub(instrumental, vocals, key, tempo_bpm, preset)
    jobs.complete(job_id, result)
    return {"job_id": job_id, "result": result}

@app.get("/v1/jobs/{job_id}/status")
async def job_status(job_id: str):
    return jobs.get(job_id)

@app.get("/v1/projects/{project_id}")
async def get_project(project_id: str):
    # Minimal stub
    return {"id": project_id, "assets": [], "status": "ok"}

class FeedbackIn(BaseModel):
    project_id: Optional[str] = None
    target: str
    rating: int
    reason: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None

@app.post("/v1/feedback")
async def feedback(payload: FeedbackIn):
    # Store or log feedback - stubbed
    return {"ok": True, "stored": payload.model_dump()}
