from fastapi import FastAPI, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from app.core.sandbox import Sandbox
from typing import List
import os

app = FastAPI(title="CodeSentinel Backend")

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
        for connection in self.active_connections:
            await connection.send_text(message)

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
        await manager.broadcast(json.dumps({"text": "> Handshaking with Docker...", "status": "WAIT", "color": "text-gray-400"}))
        graph = create_sentinel_graph(sandbox, broadcaster=manager.broadcast)
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
