from pathlib import Path
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from app.models import RunRequest, RunResponse
from app.agent import run_agent

BASE_DIR = Path(__file__).parent

app = FastAPI(title="AI Automation Agent", version="1.0.0")


@app.get("/")
def index():
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/run", response_model=RunResponse)
def run(request: RunRequest):
    try:
        result = run_agent(task=request.task, max_iterations=request.max_iterations)
        return RunResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
