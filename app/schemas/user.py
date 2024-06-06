from pydantic import BaseModel
from typing import Optional

class SellerInfo(BaseModel):
    seller_id: int
    seller_name: str
    sharing_percentage: int
    wallet_address: str
    balance: float

class User(BaseModel):
    id: int
    username: str
    email: str
    role: str
    balance: float
    password: str
    seller: Optional[SellerInfo] = None  # Add seller information as optional

class UserBase(BaseModel):
    username: str
    email: str
    role: Optional[str] = "buyer"  # Make role optional with default value
    balance: float = 0.0
    seller: Optional[SellerInfo] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserResponse(UserBase):
    id: int
    
class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    balance: float
    seller: Optional[SellerInfo] = None

    class Config:
        from_attributes = True  # or use from_attributes = True if using Pydantic v2
