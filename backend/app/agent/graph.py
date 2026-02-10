from langgraph.graph import StateGraph, END
from app.agent.state import AgentState
from app.agent.nodes import SentinelNodes
from app.core.sandbox import Sandbox

def create_sentinel_graph(sandbox: Sandbox, broadcaster=None):
    """
    Creates and compiles the LangGraph state machine.
    """
    nodes = SentinelNodes(sandbox, broadcaster)
    workflow = StateGraph(AgentState)

    # Add Nodes
    workflow.add_node("plan", nodes.plan_node)
    workflow.add_node("research", nodes.research_node)
    workflow.add_node("code", nodes.code_node)
    workflow.add_node("test", nodes.test_node)

    # Define Edges
    workflow.set_entry_point("plan")
    
    workflow.add_edge("plan", "research")
    workflow.add_edge("research", "code")
    workflow.add_edge("code", "test")

    # Conditional logic for retries / success
    def should_continue(state: AgentState):
        if state["is_complete"]:
            return "end"
        if state["retry_count"] >= 5:
            return "end"
        return "code" # Retry coding/correcting

    workflow.add_conditional_edges(
        "test",
        should_continue,
        {
            "end": END,
            "code": "code"
        }
    )

    return workflow.compile()
