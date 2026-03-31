from fastapi import FastAPI, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.core.sandbox import Sandbox
from typing import List
import os
import json
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env"))

from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize WebSocket logging
    from app.core.logger import setup_websocket_logger
    setup_websocket_logger(manager.broadcast)
    yield
    # Shutdown logic (if any) here

app = FastAPI(title="CodeSentinel Backend", lifespan=lifespan)

# Simplified Connection Manager for Log Streaming
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        stale_connections = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                stale_connections.append(connection)
        
        for stale in stale_connections:
            if stale in self.active_connections:
                self.active_connections.remove(stale)

manager = ConnectionManager()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)


@app.get("/")
def read_root():
    return {"status": "Sentinel Online", "version": "0.1.0"}

from app.services.repo_service import RepoService
from app.services.skeleton_service import SkeletonService
from app.services.github_service import GitHubService
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
        github_service = GitHubService()
        
        print(f"Starting task: {request.task} on {request.repo_url}")
        
        auth_url = github_service.get_auth_url(request.repo_url)
        clone_res = repo_service.clone_repo(auth_url)
        if clone_res["exit_code"] != 0:
            raise Exception(f"Failed to clone repository: {clone_res['output']}")
        
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
        print("[WAIT] Initializing E2B Cloud Sandbox...")
        graph = create_sentinel_graph(sandbox, broadcaster=manager.broadcast)
        final_state = await graph.ainvoke(initial_state)
        
        sandbox.stop()
        return {
            "status": "success" if final_state["is_complete"] else "failed",
            "history": final_state["history"],
            "patches": final_state["patches"]
        }
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"Error executing task: {e}")
        if hasattr(sandbox, 'sandbox') and sandbox.sandbox:
            sandbox.stop()
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    # Use PORT from environment (Render) or default to 8000
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
