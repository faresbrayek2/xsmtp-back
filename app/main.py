from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from app.routes.user import router as user_router
from app.routes.auth import router as auth_router
from app.routes.ticket import router as ticket_router
from app.routes.category import router as category_router
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
async def initialize_categories():
    categories = {
        "Accounts": [
            "Email Marketing", "Webmail Business", "Marketing Tools", "Hosting/Domain", "Games",
            "Graphic / Developer", "VPN/Socks Proxy", "Shopping", "Program", "Stream", "Dating",
            "Learning", "Torrent / File Host", "Voip / Sip", "Social Media", "Other"
        ],
        "Business": [
            "Cpanel Webmail", "Godaddy Webmail", "Office Godaddy Webmail", "Office365 Webmail",
            "Rackspace Webmail", "Ionos Webmail"
        ],
        "Leads": [
            "100% Checked Email list", "Email Only", "Combo Email:Password", "Combo Username:Password",
            "Email Access", "Combo Email:Hash", "Phone Number Only", "Combo Phone:Password", "Full Data",
            "Social Media Data"
        ],
        "Send": [
            "SMTP", "Mailers"
        ],
        "Hosts": [
            "Cpanels", "Shells", "SSH\\WHM", "RDP"
        ]
    }

    for category_name, subcategories in categories.items():
        existing_category = await db.categories.find_one({"name": category_name})
        if not existing_category:
            category = {
                "name": category_name,
                "subcategories": [{"name": subcategory} for subcategory in subcategories],
                "id": await get_next_category_id()
            }
            await db.categories.insert_one(category)

async def get_next_category_id():
    last_category = await db.categories.find_one(sort=[("id", -1)])
    return (last_category["id"] + 1) if last_category else 1

@app.get("/")
def read_root():
    return {"message": "Welcome to xSMTP Store"}

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(ticket_router, tags=["tickets"])
app.include_router(category_router, prefix="/categories", tags=["categories"])
