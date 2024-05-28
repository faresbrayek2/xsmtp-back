from pydantic import BaseModel
from typing import Optional, List

class Message(BaseModel):
    sender_id: int
    content: str
    timestamp: Optional[str] = None

class TicketCreate(BaseModel):
    title: str
    initial_message: str

class TicketUpdate(BaseModel):
    title: Optional[str] = None
    messages: Optional[List[str]] = None
    status: Optional[str] = None

class TicketResponse(BaseModel):
    id: int
    title: str
    messages: List[Message]
    status: str
    user_id: int

    class Config:
        from_attributes = True  # Pydantic v2 uses 'from_attributes' instead of 'orm_mode'
