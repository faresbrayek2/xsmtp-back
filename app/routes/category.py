from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List
import os

from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.routes.auth import get_current_user, get_current_active_admin
from app.models.user import User

router = APIRouter()

client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
db = client.xsmtp

# Helper function to get the next ID for categories
async def get_next_id():
    last_category = await db.categories.find_one(sort=[("id", -1)])
    return (last_category["id"] + 1) if last_category else 1

@router.post("/", response_model=CategoryResponse)
async def create_category(category: CategoryCreate, current_user: User = Depends(get_current_active_admin)):
    category_dict = category.dict()
    category_dict["id"] = await get_next_id()

    await db.categories.insert_one(category_dict)
    return category_dict

@router.get("/", response_model=List[CategoryResponse])
async def get_categories(current_user: User = Depends(get_current_user)):
    categories = await db.categories.find().to_list(length=100)
    return categories

@router.put("/{id}", response_model=CategoryResponse)
async def update_category(id: int, category: CategoryUpdate, current_user: User = Depends(get_current_active_admin)):
    category_dict = category.dict(exclude_unset=True)

    existing_category = await db.categories.find_one({"id": id})
    if not existing_category:
        raise HTTPException(status_code=404, detail="Category not found")

    await db.categories.update_one({"id": id}, {"$set": category_dict})
    updated_category = await db.categories.find_one({"id": id})
    return updated_category

@router.delete("/{id}", response_model=CategoryResponse)
async def delete_category(id: int, current_user: User = Depends(get_current_active_admin)):
    existing_category = await db.categories.find_one({"id": id})
    if not existing_category:
        raise HTTPException(status_code=404, detail="Category not found")

    await db.categories.delete_one({"id": id})
    return existing_category
