from typing import Dict
from app.core.sandbox import Sandbox

class RepoService:
    def __init__(self, sandbox: Sandbox):
        self.sandbox = sandbox

    def clone_repo(self, repo_url: str, dest_path: str = "/repo") -> Dict[str, str]:
        """Clone a GitHub repository into the sandbox."""
        print(f"Preparing environment and cloning {repo_url}...")
        # Combine into one command to ensure sequential execution and captured logs
        command = f"apt-get update && apt-get install -y git && git clone {repo_url} {dest_path}"
        result = self.sandbox.execute(f"bash -c '{command}'")
        return result

    def list_files(self, path: str = "/repo") -> Dict[str, str]:
        """List files in the cloned repository."""
        return self.sandbox.execute(f"find {path} -maxdepth 2 -not -path '*/.*'")
