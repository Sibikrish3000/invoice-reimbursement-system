from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ChatMessage(BaseModel):
    role: str = Field(..., description="Role of the message sender (user/assistant)")
    content: str = Field(..., description="Content of the message")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class ChatRequest(BaseModel):
    query: str = Field(..., description="User's query about invoice reimbursements")
    chat_history: Optional[List[ChatMessage]] = Field(default=None, description="Previous chat messages for context")

class ChatResponse(BaseModel):
    response: str = Field(..., description="Assistant's response in markdown format")
    relevant_invoices: Optional[List[str]] = Field(default=None, description="List of relevant invoice IDs referenced in the response")
    chat_history: List[ChatMessage] = Field(..., description="Updated chat history including the new exchange") 