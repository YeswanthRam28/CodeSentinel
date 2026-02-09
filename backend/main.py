from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from app.core.sandbox import Sandbox
import os

app = FastAPI(title="CodeSentinel Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "Sentinel Online", "version": "0.1.0"}

from app.services.repo_service import RepoService
from app.services.skeleton_service import SkeletonService
from pydantic import BaseModel

class RepoRequest(BaseModel):
    repo_url: str

@app.post("/analyze-repo")
async def analyze_repo(request: RepoRequest):
    """Phase 2: Clone and analyze a repository structure."""
    sandbox = Sandbox()
    try:
        sandbox.start()
        
        repo_service = RepoService(sandbox)
        skeleton_service = SkeletonService(sandbox)
        
        # 1. Clone
        clone_res = repo_service.clone_repo(request.repo_url)
        if clone_res["exit_code"] != 0:
            return {"status": "error", "message": "Clone failed", "output": clone_res["output"]}
            
        # 2. Analyze
        skeleton = skeleton_service.generate_skeleton()
        
        sandbox.stop()
        return {
            "status": "success",
            "repo": request.repo_url,
            "skeleton": skeleton
        }
    except Exception as e:
        if sandbox.container:
            sandbox.stop()
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
