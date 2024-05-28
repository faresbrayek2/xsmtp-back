from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient
from typing import List
from app.models.user import User
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate
from app.routes.auth import get_current_user, get_current_active_admin, get_current_active_support
import os

router = APIRouter()

client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
db = client.xsmtp

async def update_product_count(category_name: str, subcategory_name: str, increment: int):
    category = await db.categories.find_one({"name": category_name})
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    subcategory_index = next((index for (index, d) in enumerate(category["subcategories"]) if d["name"] == subcategory_name), None)
    if subcategory_index is None:
        raise HTTPException(status_code=404, detail="Subcategory not found")

    category["subcategories"][subcategory_index]["product_count"] += increment
    await db.categories.update_one({"name": category_name}, {"$set": {"subcategories": category["subcategories"]}})

@router.post("/", response_model=ProductResponse)
async def create_product(product: ProductCreate, current_user: User = Depends(get_current_user)):
    product_dict = product.dict()
    product_dict["user_id"] = current_user.id

    await db.products.insert_one(product_dict)
    await update_product_count(product.category, product.subcategory, 1)
    return product_dict

@router.put("/{id}", response_model=ProductResponse)
async def update_product(id: str, product: ProductUpdate, current_user: User = Depends(get_current_user)):
    product_dict = product.dict(exclude_unset=True)
    existing_product = await db.products.find_one({"_id": id})
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")

    if existing_product["user_id"] != current_user.id and current_user.role not in ["admin", "support"]:
        raise HTTPException(status_code=403, detail="Not authorized to update this product")

    if "category" in product_dict or "subcategory" in product_dict:
        if existing_product["category"] != product_dict["category"] or existing_product["subcategory"] != product_dict["subcategory"]:
            await update_product_count(existing_product["category"], existing_product["subcategory"], -1)
            await update_product_count(product_dict["category"], product_dict["subcategory"], 1)

    await db.products.update_one({"_id": id}, {"$set": product_dict})
    updated_product = await db.products.find_one({"_id": id})
    return updated_product

@router.delete("/{id}", response_model=ProductResponse)
async def delete_product(id: str, current_user: User = Depends(get_current_user)):
    existing_product = await db.products.find_one({"_id": id})
    if not existing_product:
        raise HTTPException(status_code=404, detail="Product not found")

    if existing_product["user_id"] != current_user.id and current_user.role not in ["admin", "support"]:
        raise HTTPException(status_code=403, detail="Not authorized to delete this product")

    await db.products.delete_one({"_id": id})
    await update_product_count(existing_product["category"], existing_product["subcategory"], -1)
    return existing_product
