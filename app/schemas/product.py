from pydantic import BaseModel
from typing import Optional

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category: str
    subcategory: str

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: str
    user_id: int

    class Config:
        from_attributes = True
