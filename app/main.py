from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from app.routes.user import router as user_router
from app.routes.auth import router as auth_router
from app.routes.ticket import router as ticket_router
from app.routes.category import router as category_router
from app.routes.product import router as product_router
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
SECRET_KEY = os.getenv("SECRET_KEY")

app = FastAPI()

# Database connection
client = AsyncIOMotorClient(MONGODB_URL)
db = client.xsmtp

@app.on_event("startup")
async def initialize_collections():
    collections = await db.list_collection_names()
    if "users" not in collections:
        await db.create_collection("users")

async def get_next_id():
    last_user = await db.users.find_one(sort=[("id", -1)])
    return (last_user["id"] + 1) if last_user else 1

@app.get("/")
def read_root():
    return {"message": "Welcome to xSMTP Store"}

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(ticket_router, tags=["tickets"])
app.include_router(category_router, prefix="/categories", tags=["categories"])
app.include_router(product_router, prefix="/products", tags=["products"])
