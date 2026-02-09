import docker
import os
import tarfile
import io
from typing import Optional, Dict

class Sandbox:
    def __init__(self, image: str = "python:3.11-slim"):
        self.client = docker.from_env()
        self.image = image
        self.container = None

    def start(self):
        """Start an ephemeral Docker container."""
        print(f"Starting container: {self.image}")
        self.container = self.client.containers.run(
            self.image,
            command="tail -f /dev/null",
            detach=True,
            remove=True,
            network_disabled=False # Needed for cloning repos
        )
        return self.container.id

    def execute(self, command: str, workdir: str = "/") -> Dict[str, str]:
        """Execute a command inside the container and capture output."""
        if not self.container:
            raise Exception("Container not started.")
        
        result = self.container.exec_run(command, workdir=workdir)
        return {
            "exit_code": result.exit_code,
            "output": result.output.decode("utf-8")
        }

    def stop(self):
        """Stop and remove the container."""
        if self.container:
            self.container.stop()
            self.container = None

    def upload_file(self, content: str, filename: str, path: str = "/"):
        """Upload a file to the container."""
        if not self.container:
            raise Exception("Container not started.")
        
        # Create a tar archive in memory
        tar_stream = io.BytesIO()
        with tarfile.open(fileobj=tar_stream, mode='w') as tar:
            content_bytes = content.encode('utf-8')
            tarinfo = tarfile.TarInfo(name=filename)
            tarinfo.size = len(content_bytes)
            tar.addfile(tarinfo, io.BytesIO(content_bytes))
        
        tar_stream.seek(0)
        self.container.put_archive(path, tar_stream)

# Usage Example (To be moved to tests later):
# sandbox = Sandbox()
# sandbox.start()
# print(sandbox.execute("pip --version"))
# sandbox.stop()
