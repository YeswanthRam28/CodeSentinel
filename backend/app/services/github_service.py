import httpx
import os
import base64
from typing import Dict, Any, Optional

class GitHubService:
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }

    async def create_pull_request(self, repo_url: str, title: str, body: str, head: str, base: str = "main") -> Dict[str, Any]:
        """
        Note: This implementation assumes the agent has already pushed changes to a branch 
        inside the sandbox or we handle the push via API.
        For simplicity in this step, we'll implement the API call to open the PR.
        """
        if not self.token:
            return {"error": "GITHUB_TOKEN not configured"}

        # Extract owner and repo from URL
        # URL format: https://github.com/owner/repo
        parts = repo_url.rstrip("/").split("/")
        owner = parts[-2]
        repo = parts[-1]
        
        api_url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
        
        data = {
            "title": title,
            "body": body,
            "head": head,
            "base": base
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(api_url, headers=self.headers, json=data)
            if response.status_code == 201:
                return response.json()
            else:
                return {"error": f"Failed to create PR: {response.text}"}

    def get_auth_url(self, repo_url: str) -> str:
        """Injects token into repo URL for authenticated git operations."""
        if not self.token:
            return repo_url
        return repo_url.replace("https://", f"https://x-access-token:{self.token}@")
