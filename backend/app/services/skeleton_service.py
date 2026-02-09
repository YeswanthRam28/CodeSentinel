import json
from typing import Dict, Any
from app.core.sandbox import Sandbox

class SkeletonService:
    def __init__(self, sandbox: Sandbox):
        self.sandbox = sandbox

    def install_dependencies(self):
        """Install AST parsing tools inside the sandbox."""
        # Using a simple python script with ast module for Python, 
        # but for more languages we'd install tree-sitter-cli or similar.
        # For now, let's start with a robust Python-based skeleton generator 
        # that we inject into the container.
        pass

    def generate_skeleton(self, repo_path: str = "/repo") -> Dict[str, Any]:
        """
        Generates a structural map of the repository.
        This script is injected and executed inside the sandbox.
        """
        skeleton_script = """
import os
import ast
import json

def get_python_skeleton(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        tree = ast.parse(f.read())
    
    skeleton = {
        "classes": [],
        "functions": []
    }
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            methods = [n.name for n in node.body if isinstance(n, ast.FunctionDef)]
            skeleton["classes"].append({"name": node.name, "methods": methods})
        elif isinstance(node, ast.FunctionDef) and not any(isinstance(parent, ast.ClassDef) for parent in ast.walk(node)): # Top level functions
             skeleton["functions"].append(node.name)
             
    return skeleton

repo_map = {}
for root, dirs, files in os.walk("."):
    if '.git' in dirs: dirs.remove('.git')
    for file in files:
        if file.endswith('.py'):
            rel_path = os.path.join(root, file)
            try:
                repo_map[rel_path] = get_python_skeleton(rel_path)
            except:
                repo_map[rel_path] = "error_parsing"

print(json.dumps(repo_map))
"""
        self.sandbox.upload_file(skeleton_script, "skeleton_gen.py", "/tmp")
        result = self.sandbox.execute("python3 /tmp/skeleton_gen.py", workdir=repo_path)
        
        try:
            return json.loads(result["output"])
        except:
            return {"error": "Failed to parse skeleton output", "raw": result["output"]}
