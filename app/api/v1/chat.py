from fastapi import APIRouter, HTTPException
from app.models import ChatRequest, ChatResponse
from app.agent import AgentManager

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest):
    try:
        agent = AgentManager.get_agent()

        if payload.message.lower() == "clear":
            agent.clear_conversation_history()
            return ChatResponse(response="Conversation history cleared.")

        result = await agent.run(payload.message)
        return ChatResponse(response=result)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
