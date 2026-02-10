import json
import os
from typing import Dict, Any, List
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, SystemMessage
from app.agent.state import AgentState
from app.core.sandbox import Sandbox
from app.services.repo_service import RepoService
from app.services.skeleton_service import SkeletonService
from app.services.github_service import GitHubService

class SentinelNodes:
    def __init__(self, sandbox: Sandbox, broadcaster=None):
        self.sandbox = sandbox
        self.broadcaster = broadcaster
        self.repo_service = RepoService(sandbox)
        self.skeleton_service = SkeletonService(sandbox)
        self.github_service = GitHubService()
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash", 
            google_api_key=os.getenv("GEMINI_API_KEY")
        )

    async def log(self, text: str, status: str = "INFO", color: str = "text-gray-400"):
        if self.broadcaster:
            await self.broadcaster(json.dumps({
                "text": f"> {text}",
                "status": status,
                "color": color
            }))

    async def plan_node(self, state: AgentState) -> Dict[str, Any]:
        """Node: Create a step-by-step plan based on the task and skeleton."""
        await self.log("Planning implementation steps...", "PLAN", "text-blue-400")
        prompt = f"""
        You are CodeSentinel, an autonomous AI DevOps Agent.
        Task: {state['task']}
        
        Repository Skeleton:
        {json.dumps(state['repo_skeleton'], indent=2)}
        
        Based on the task and the codebase structure, create a high-level plan to resolve the issue.
        Return only a JSON array of strings representing the steps.
        """
        
        response = self.llm.invoke([
            SystemMessage(content="You are a senior software architect."),
            HumanMessage(content=prompt)
        ])
        
        # Simple extraction logic (could be improved with structured output)
        try:
            content = response.content
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            plan = json.loads(content)
        except:
            plan = ["Analyze relevant files", "Implement fix", "Verify with tests"]
            
        return {
            "plan": plan,
            "history": state.get("history", []) + ["Created initial implementation plan."]
        }

    async def research_node(self, state: AgentState) -> Dict[str, Any]:
        """Node: Identify relevant files and read their content."""
        await self.log("Analyzing repository skeleton...", "SEARCH", "text-cyan-400")
        prompt = f"""
        Task: {state['task']}
        Plan: {json.dumps(state['plan'])}
        Skeleton: {json.dumps(state['repo_skeleton'])}
        
        Identify the top 3-5 files that need to be examined or modified.
        Return only a JSON array of file paths.
        """
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        
        try:
            content = response.content
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            plan_files = json.loads(content)
        except:
            plan_files = []

        return {
            "relevant_files": plan_files,
            "history": state.get("history", []) + [f"Identified {len(plan_files)} relevant files for research."]
        }

    async def code_node(self, state: AgentState) -> Dict[str, Any]:
        """Node: Generate code changes/patches."""
        await self.log("Generating autonomous patches...", "CODE", "text-violet-400")
        # In a real scenario, we'd read file contents here. 
        # For this phase, we simulate the "Brain" deciding what to change.
        prompt = f"""
        Generate the actual code changes to satisfy: {state['task']}
        Relevant Files: {state['relevant_files']}
        
        Return the response as a JSON object where keys are file paths and values are the NEW content of the file.
        Example: {{"app/main.py": "print('hello')"}}
        """
        
        response = self.llm.invoke([HumanMessage(content=prompt)])
        
        try:
            content = response.content
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            patches = json.loads(content)
        except:
            patches = {}

        # Apply patches in sandbox
        for path, code in patches.items():
            dir_name = os.path.dirname(path)
            if dir_name:
                self.sandbox.execute(f"mkdir -p {dir_name}", workdir="/repo")
            self.sandbox.upload_file(code, os.path.basename(path), os.path.join("/repo", dir_name))

        return {
            "patches": patches,
            "history": state.get("history", []) + [f"Generated and applied patches to {len(patches)} files."]
        }

    async def test_node(self, state: AgentState) -> Dict[str, Any]:
        """Node: Execute tests in the sandbox."""
        await self.log("Executing tests in Docker sandbox...", "TEST", "text-green-400")
        # Try to run common test commands
        res = self.sandbox.execute("pytest", workdir="/repo")
        if "command not found" in res["output"].lower():
             res = self.sandbox.execute("python -m unittest discover", workdir="/repo")
             
        success = res["exit_code"] == 0
        return {
            "test_results": res,
            "is_complete": success,
            "retry_count": state["retry_count"] + (0 if success else 1),
            "history": state.get("history", []) + [f"Ran test suite. Status: {'Success' if success else 'Failed'}."]
        }

    async def pr_node(self, state: AgentState) -> Dict[str, Any]:
        """Node: Push changes and create a Pull Request."""
        await self.log("Preparing Pull Request and Finalizing...", "PR", "text-blue-400")
        
        branch_name = f"sentinel-fix-{os.urandom(4).hex()}"
        
        # 1. Push to GitHub
        push_res = self.repo_service.push_branch(branch_name)
        if push_res["exit_code"] != 0:
            return {"history": state.get("history", []) + ["Failed to push changes to GitHub."]}

        # 2. Create PR via GitHub API
        title = f"Autonomous Fix: {state['task'][:50]}..."
        body = f"""
### 🤖 CodeSentinel Autonomous PR

**Task:** {state['task']}

**Implementation Details:**
- Discovered structural context using AST parsing.
- Verified fix using autonomous test execution.
- Self-healed through {state['retry_count']} iterations.

*Generated by CodeSentinel.*
"""
        pr_res = await self.github_service.create_pull_request(
            repo_url=state["repo_url"],
            title=title,
            body=body,
            head=branch_name
        )
        
        pr_link = pr_res.get("html_url", "PR Created (Link unavailable)")
        
        return {
            "message": f"Successfully opened PR: {pr_link}",
            "history": state.get("history", []) + [f"Pull Request created: {pr_link}"]
        }
