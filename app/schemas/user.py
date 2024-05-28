from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str
    email: str

class User(BaseModel):
    id: int
    username: str
    role: str
    email: str
    balance: float

    class Config:
        orm_mode = True # Pydantic v2 uses 'orm_mode' instead of 'from_attributes'
