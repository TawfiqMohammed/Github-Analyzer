from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Agentic GitHub Analyzer")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the absolute path to frontend directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(os.path.dirname(BASE_DIR), "frontend")

# Mount static files (CSS, JS)
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# Serve HTML pages
@app.get("/")
async def serve_index():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.get("/analyze.html")
async def serve_analyze():
    return FileResponse(os.path.join(FRONTEND_DIR, "analyze.html"))

@app.get("/dashboard.html")
async def serve_dashboard():
    return FileResponse(os.path.join(FRONTEND_DIR, "dashboard.html"))

@app.get("/mlops.html")
async def serve_mlops():
    return FileResponse(os.path.join(FRONTEND_DIR, "mlops.html"))

# API Endpoints (we'll implement these later)
@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "Backend is running!"}

@app.post("/api/analyze")
async def analyze_repo(repo_data: dict):
    # We'll implement this with agents later
    return {
        "status": "success",
        "message": "Analysis started",
        "session_id": "test-123"
    }

# Run with: uvicorn main:app --reload