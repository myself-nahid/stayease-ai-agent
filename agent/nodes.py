from langchain_core.messages import AIMessage
from langgraph.prebuilt.tool_node import ToolNode
from agent.state import AgentState
from agent.tools import stay_ease_tools

# Mocking LLM for the skeleton structure
class MockLLM:
    def invoke(self, messages):
        return AIMessage(content="How can I help you with StayEase today?")

llm = MockLLM()

def chatbot_node(state: AgentState) -> dict:
    """Calls the LLM with the current conversation history."""
    response = llm.invoke(state["messages"])
    
    if "escalate" in str(response.content).lower():
        return {"escalate_to_human": True}
        
    return {"messages":[response]}

tools_node = ToolNode(tools=stay_ease_tools)

def human_escalation_node(state: AgentState) -> dict:
    """Handles routing the conversation to a human agent."""
    return {
        "messages": [AIMessage(content="Transferring you to a human agent.")],
        "escalate_to_human": True
    }