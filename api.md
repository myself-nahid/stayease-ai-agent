# StayEase API Contract

## 1. POST /api/chat/{conversation_id}/message
Sends a guest message to the agent.

### Request Schema:
```json
{
  "message": "string"
}
```

### Realistic Example:
```
POST /api/chat/123e4567-e89b-12d3-a456-426614174000/message
```

```json
{
  "message": "I need a place in Sylhet for 3 guests from Nov 1 to Nov 4."
}
```

### Response (200 OK):
```json
{
  "response": "I found 2 available properties in Sylhet! \n1. Tea Garden Retreat - 6000 BDT/night.\n2. Hilltop Cabin - 4500 BDT/night.\nWould you like details on either?",
  "escalated": false
}
```

### Error Responses:
- **400 Bad Request**: Invalid payload.  
- **502 Bad Gateway**: LLM provider timeout.  


---

## 2. GET /api/chat/{conversation_id}/history
Retrieves conversation history.

### Realistic Example:
```
GET /api/chat/123e4567-e89b-12d3-a456-426614174000/history
```

### Response (200 OK):
```json
{
  "conversation_id": "123e4567-e89b-12d3-a456-426614174000",
  "messages": [
    {
      "role": "user",
      "content": "Hi, any properties in Sreemangal?",
      "timestamp": "2026-04-27T14:30:00Z"
    },
    {
      "role": "agent",
      "content": "Yes! What dates are you planning?",
      "timestamp": "2026-04-27T14:30:05Z"
    }
  ]
}
```

### Error Responses:
- **404 Not Found**: Conversation ID does not exist.