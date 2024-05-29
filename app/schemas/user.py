from pydantic import BaseModel
from typing import Optional

class SellerInfo(BaseModel):
    seller_id: Optional[int] = None
    seller_name: Optional[str] = None
    sharing_percentage: Optional[float] = None
    wallet_address: Optional[str] = None

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

    class Config:
        from_attributes = True  # or use from_attributes = True if using Pydantic v2
