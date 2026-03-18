from langgraph.graph import StateGraph

from app.agents.state import FraudState
from app.agents.fraud_nodes import (
    analyze_node,
    explanation_node,
    persist_node
)


def build_graph():

    builder = StateGraph(FraudState)

    # nodes
    builder.add_node("analyze", analyze_node)
    builder.add_node("explain", explanation_node)
    builder.add_node("persist", persist_node)

    # flow
    builder.set_entry_point("analyze")

    builder.add_edge("analyze", "explain")
    builder.add_edge("explain", "persist")

    return builder.compile()