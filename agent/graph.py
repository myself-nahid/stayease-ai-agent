from langgraph.graph import StateGraph, START, END
from agent.state import AgentState
from agent.nodes import chatbot_node, tools_node, human_escalation_node

def route_from_chatbot(state: AgentState):
    """Conditional router based on chatbot output."""
    # 1. Check if the bot decided to escalate
    if state.get("escalate_to_human"):
        return "escalate"
    
    # 2. Bulletproof manual check for tool calls (No need for langgraph.prebuilt)
    messages = state.get("messages", [])
    if messages:
        last_message = messages[-1]
        # If the LLM generated tool calls, route to the tools node
        if hasattr(last_message, "tool_calls") and len(last_message.tool_calls) > 0:
            return "tools"
            
    # 3. Otherwise, end the graph and return to user
    return END

# Construct the graph
builder = StateGraph(AgentState)

builder.add_node("chatbot", chatbot_node)
builder.add_node("tools", tools_node)
builder.add_node("escalate", human_escalation_node)

# Set edges
builder.add_edge(START, "chatbot")

builder.add_conditional_edges(
    "chatbot", 
    route_from_chatbot, 
    {"tools": "tools", "escalate": "escalate", END: END}
)

builder.add_edge("tools", "chatbot")
builder.add_edge("escalate", END)

graph = builder.compile()