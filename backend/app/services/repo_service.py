from typing import Dict
from app.core.sandbox import Sandbox

class RepoService:
    def __init__(self, sandbox: Sandbox):
        self.sandbox = sandbox

    def clone_repo(self, repo_url: str, dest_path: str = "/home/user/repo") -> Dict[str, str]:
        """Clone a GitHub repository into the sandbox."""
        print(f"Preparing environment and cloning {repo_url}...")
        # E2B sandboxes (base) usually have git and python pre-installed
        command = f"git clone {repo_url} {dest_path}"
        result = self.sandbox.execute(f"bash -c '{command}'")
        return result

    def push_branch(self, branch_name: str) -> Dict[str, str]:
        """Configure git user and push current changes to a new branch."""
        print(f"Pushing changes to branch: {branch_name}...")
        commands = [
            'git config --global user.email "sentinel@codesentinel.ai"',
            'git config --global user.name "CodeSentinel Agent"',
            f'git checkout -b {branch_name}',
            'git add .',
            'git commit -m "feat: autonomous bug fix by CodeSentinel"',
            f'git push origin {branch_name}'
        ]
        full_command = " && ".join(commands)
        result = self.sandbox.execute(f"bash -c '{full_command}'", workdir="/home/user/repo")
        return result

    def list_files(self, path: str = "/home/user/repo") -> Dict[str, str]:
        """List files in the cloned repository."""
        return self.sandbox.execute(f"find {path} -maxdepth 2 -not -path '*/.*'")
