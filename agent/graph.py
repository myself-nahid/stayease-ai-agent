from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import tools_condition
from agent.state import AgentState
from agent.nodes import chatbot_node, tools_node, human_escalation_node

def route_from_chatbot(state: AgentState):
    """Conditional router based on chatbot output."""
    if state.get("escalate_to_human"):
        return "escalate"
    if tools_condition(state) == "tools":
        return "tools"
    return END

builder = StateGraph(AgentState)

builder.add_node("chatbot", chatbot_node)
builder.add_node("tools", tools_node)
builder.add_node("escalate", human_escalation_node)

builder.add_edge(START, "chatbot")
builder.add_conditional_edges("chatbot", route_from_chatbot, {"tools": "tools", "escalate": "escalate", END: END})
builder.add_edge("tools", "chatbot")
builder.add_edge("escalate", END)

graph = builder.compile()