from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str
    password: str
    role: str
    email: str
    balance: float
