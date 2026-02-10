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

from app.agent.graph import create_sentinel_graph
from app.agent.state import AgentState

class TaskRequest(BaseModel):
    repo_url: str
    task: str

@app.post("/execute-task")
async def execute_task(request: TaskRequest):
    """Phase 3: Trigger the full autonomous Agentic Workflow."""
    sandbox = Sandbox()
    try:
        sandbox.start()
        
        # 1. Initialize State
        repo_service = RepoService(sandbox)
        skeleton_service = SkeletonService(sandbox)
        
        print(f"Starting task: {request.task} on {request.repo_url}")
        
        repo_service.clone_repo(request.repo_url)
        skeleton = skeleton_service.generate_skeleton()
        
        initial_state: AgentState = {
            "task": request.task,
            "repo_url": request.repo_url,
            "repo_skeleton": skeleton,
            "plan": [],
            "relevant_files": [],
            "patches": {},
            "test_results": None,
            "retry_count": 0,
            "history": [f"Task assigned: {request.task}"],
            "is_complete": False,
            "message": ""
        }
        
        # 2. Run Graph
        graph = create_sentinel_graph(sandbox)
        final_state = await graph.ainvoke(initial_state)
        
        sandbox.stop()
        return {
            "status": "success" if final_state["is_complete"] else "failed",
            "history": final_state["history"],
            "patches": final_state["patches"]
        }
    except Exception as e:
        if sandbox.container:
            sandbox.stop()
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
