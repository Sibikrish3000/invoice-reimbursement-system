from fastapi import APIRouter, HTTPException
from app.api.models.chat import ChatRequest, ChatResponse
from app.services.chatbot import Chatbot
from app.services.vector_store import VectorStore

router = APIRouter()
vector_store = VectorStore()
chatbot = Chatbot(vector_store)

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response = await chatbot.process_query(
            query=request.query,
            chat_history=request.chat_history
        )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing chat request: {str(e)}"
        ) 