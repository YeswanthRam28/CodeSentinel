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

@app.post("/test-sandbox")
async def test_sandbox(background_tasks: BackgroundTasks):
    """Temporary endpoint to verify Docker sandbox functionality."""
    try:
        sandbox = Sandbox()
        sandbox.start()
        res = sandbox.execute("python --version")
        sandbox.stop()
        return {"status": "success", "output": res["output"]}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
