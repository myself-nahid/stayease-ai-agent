from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
from agent.graph import graph

app = FastAPI(title="StayEase AI Agent API")

class MessageRequest(BaseModel):
    message: str

@app.post("/api/chat/{conversation_id}/message")
async def send_message(conversation_id: str, req: MessageRequest):
    """Endpoint to send a message to the LangGraph agent."""
    try:
        # In production: Fetch state from PostgreSQL here
        initial_state = {"messages": [HumanMessage(content=req.message)], "escalate_to_human": False}
        
        # Invoke the LangGraph agent
        result = graph.invoke(initial_state)
        
        # In production: Save updated state to PostgreSQL here
        last_message = result["messages"][-1].content
        
        return {
            "response": last_message,
            "escalated": result.get("escalate_to_human", False)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/chat/{conversation_id}/history")
async def get_history(conversation_id: str):
    """Endpoint to retrieve conversation history."""
    # Mocking DB retrieval for the skeleton
    return {
        "conversation_id": conversation_id,
        "messages":[
            {"role": "user", "content": "Hi", "timestamp": "2026-04-27T10:00:00Z"}
        ]
    }