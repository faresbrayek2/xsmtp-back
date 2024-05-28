from pydantic import BaseModel
from typing import Optional, List

class Subcategory(BaseModel):
    name: str

class CategoryBase(BaseModel):
    name: str
    subcategories: Optional[List[Subcategory]] = []

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int

    class Config:
        from_attributes = True
