from typing import List, TypedDict, Optional, Dict, Any

class AgentState(TypedDict):
    """
    State representing the current status of the CodeSentinel agent workflow.
    """
    # The original task/issue description
    task: str
    
    # URL of the repository being worked on
    repo_url: str
    
    # Structural map of the repository (from SkeletonService)
    repo_skeleton: Dict[str, Any]
    
    # The current plan (list of steps)
    plan: List[str]
    
    # List of files identified as relevant during research
    relevant_files: List[str]
    
    # The current set of code changes/patches
    patches: Dict[str, str]
    
    # Results of the latest test run
    test_results: Optional[Dict[str, Any]]
    
    # Number of retries attempted for the current task
    retry_count: int
    
    # History of actions taken for logging/UI display
    history: List[str]
    
    # Whether the task is completed successfully
    is_complete: bool
    
    # Final message or PR description
    message: str
