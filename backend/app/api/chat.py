from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.services.rag_service import RAGService

router = APIRouter()
rag_service = RAGService()

class Message(BaseModel):
    role: str
    content: str
    timestamp: Optional[str] = None

class ChatRequest(BaseModel):
    message: str
    conversation_history: Optional[List[Message]] = []
    session_id: Optional[str] = None

class Source(BaseModel):
    title: str
    content: str
    url: str
    source_type: str  # "vidal" or "meddispar"
    relevance_score: float

class ChatResponse(BaseModel):
    response: str
    sources: List[Source]
    session_id: str
    timestamp: str
    tokens_used: Optional[int] = None

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint - sends user message and returns AI response with sources
    """
    try:
        if not request.message.strip():
            raise HTTPException(status_code=400, detail="Message cannot be empty")
        
        # Generate response using RAG
        result = await rag_service.generate_response(
            query=request.message,
            conversation_history=request.conversation_history,
            session_id=request.session_id
        )
        
        return ChatResponse(
            response=result["response"],
            sources=result["sources"],
            session_id=result["session_id"],
            timestamp=datetime.utcnow().isoformat(),
            tokens_used=result.get("tokens_used")
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating response: {str(e)}")

@router.post("/clear")
async def clear_session(session_id: str):
    """Clear conversation history for a session"""
    try:
        rag_service.clear_session(session_id)
        return {"status": "success", "message": "Session cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing session: {str(e)}")
