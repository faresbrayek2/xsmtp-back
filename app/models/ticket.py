from pydantic import BaseModel
from typing import Optional, List

class Ticket(BaseModel):
    id: int
    title: str
    messages: List[Message]
    status: str
    user_id: int

    class Config:
        from_attributes = True  # Pydantic v2 uses 'from_attributes' instead of 'orm_mode'