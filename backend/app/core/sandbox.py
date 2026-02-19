from e2b import Sandbox as E2BSandbox
import os
import io
from typing import Optional, Dict

class Sandbox:
    def __init__(self, template: str = "base"):
        self.template = template
        self.sandbox: Optional[E2BSandbox] = None

    def start(self):
        """Start an ephemeral E2B cloud sandbox."""
        print(f"Starting cloud sandbox (E2B)...")
        self.sandbox = E2BSandbox.create(template=self.template)
        return self.sandbox.sandbox_id

    def execute(self, command: str, workdir: str = "/home/user") -> Dict[str, str]:
        """Execute a command inside the cloud sandbox and capture output."""
        if not self.sandbox:
            raise Exception("Sandbox not started.")
        
        # E2B commands run as 'user' by default, usually in /home/user
        # We wrap the command to ensure we are in the right workdir
        cmd = f"cd {workdir} && {command}"
        print(f"Executing: {cmd}")
        
        result = self.sandbox.commands.run(cmd)
        
        return {
            "exit_code": result.exit_code,
            "output": result.stdout + result.stderr
        }

    def stop(self):
        """Close the cloud sandbox."""
        if self.sandbox:
            self.sandbox.kill()
            self.sandbox = None

    def upload_file(self, content: str, filename: str, path: str = "/home/user"):
        """Upload a file to the cloud sandbox."""
        if not self.sandbox:
            raise Exception("Sandbox not started.")
        
        # Ensure path exists
        self.sandbox.commands.run(f"mkdir -p {path}")
        
        # Join path properly for Linux
        full_path = f"{path.rstrip('/')}/{filename}"
        
        # Write file content
        self.sandbox.files.write(full_path, content)

    @property
    def sandbox_id(self):
        return self.sandbox.sandbox_id if self.sandbox else None
