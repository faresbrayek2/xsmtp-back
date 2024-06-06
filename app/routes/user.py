from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List
from pydantic import BaseModel

from app.schemas.user import UserCreate, UserResponse
from app.routes.auth import get_current_user, get_current_active_admin, get_next_id, get_password_hash
import os

router = APIRouter()

client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
db = client.xsmtp

class UserRoleUpdate(BaseModel):
    role: str

async def get_next_seller_id():
    last_user = await db.users.find_one({"seller.seller_id": {"$exists": True}}, sort=[("seller.seller_id", -1)])
    return (last_user["seller"]["seller_id"] + 1) if last_user else 1

@router.post("/", response_model=UserResponse)
async def create_user(user: UserCreate):
    user_dict = user.dict()
    user_dict["role"] = "buyer"  # Default role
    user_dict["id"] = await get_next_id()
    user_dict["balance"] = 0.0

    hashed_password = get_password_hash(user_dict["password"])
    user_dict["password"] = hashed_password

    await db.users.insert_one(user_dict)
    return UserResponse(**user_dict)

@router.get("/{id}", response_model=UserResponse)
async def get_user(id: int, current_user: UserResponse = Depends(get_current_user)):
    user = await db.users.find_one({"id": id})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return UserResponse(**user)

@router.get("/", response_model=List[UserResponse])
async def get_users(current_user: UserResponse = Depends(get_current_user)):
    users = await db.users.find().to_list(length=100)
    return [UserResponse(**user) for user in users]

@router.put("/{id}/role", response_model=UserResponse)
async def update_user_role(id: int, user_role_update: UserRoleUpdate, current_user: UserResponse = Depends(get_current_active_admin)):
    user_dict = user_role_update.dict()

    existing_user = await db.users.find_one({"id": id})
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_role_update.role == "seller":
        seller_info = {
            "seller_id": await get_next_seller_id(),
            "seller_name": f"Seller{await get_next_seller_id()}",
            "sharing_percentage": 50,  # Predefined value
            "wallet_address": "default_wallet_address",  # Predefined value
            "balance": 0.0  # Initial balance for sellers
        }
        user_dict["seller"] = seller_info

    await db.users.update_one({"id": id}, {"$set": user_dict})
    updated_user = await db.users.find_one({"id": id})
    return UserResponse(**updated_user)
