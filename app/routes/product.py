from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Union
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import os
from dotenv import load_dotenv
from app.schemas.product import (
    ShellsInput, CPanelInput, SSHWHMInput, RDPInput, SMTPInput, MailersInput,
    LeadsInput, BusinessInput, AccountsInput,
    Shells, CPanel, SSHWHM, RDP, SMTP, Mailers, Leads, Business, Accounts
)
from app.routes.auth import get_current_active_seller
from app.schemas.user import UserResponse
from app.utils import extract_tld, check_ssl, lookup_ip, get_hosting, get_host_info, get_seo_data

load_dotenv()

router = APIRouter()

client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
db = client.xsmtp

# Define the full_schemas dictionary
full_schemas = {
    "shells": Shells,
    "cpanel": CPanel,
    "sshwhm": SSHWHM,
    "rdp": RDP,
    "smtp": SMTP,
    "mailers": Mailers,
    "leads": Leads,
    "business": Business,
    "accounts": Accounts
}

async def get_next_product_id(product_type: str):
    last_product = await db[product_type].find_one(sort=[("id", -1)])
    return (last_product["id"] + 1) if last_product else 1

async def create_generic_product(product_dict: dict, product_type: str, seller_name: str):
    seo_data = get_seo_data(product_dict.get("url", ""))
    product_dict.update({
        "id": await get_next_product_id(product_type),
        "seller": seller_name,
        "date_created": datetime.utcnow(),
        "tld": extract_tld(product_dict.get("url", "")),
        "ssl": check_ssl(product_dict.get("url", "")),
        "location": lookup_ip(product_dict.get("url", "")),
        "hosting": get_hosting(product_dict.get("url", "")),
        "host_info": get_host_info(product_dict.get("url", "")),
        "seo_rank_da": seo_data.get("seo_rank_da"),
        "seo_info": seo_data.get("seo_info")
    })

    full_product = full_schemas[product_type](**product_dict)
    await db[product_type].insert_one(full_product.dict())
    return full_product

@router.post("/shells", response_model=Shells)
async def create_shells_product(product: ShellsInput, current_user: UserResponse = Depends(get_current_active_seller)):
    if current_user.seller is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not a seller")
    product_dict = product.dict()
    seller_name = current_user.seller.seller_name
    return await create_generic_product(product_dict, "shells", seller_name)

@router.post("/cpanel", response_model=CPanel)
async def create_cpanel_product(product: CPanelInput, current_user: UserResponse = Depends(get_current_active_seller)):
    if current_user.seller is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not a seller")
    product_dict = product.dict()
    seller_name = current_user.seller.seller_name
    return await create_generic_product(product_dict, "cpanel", seller_name)

@router.post("/sshwhm", response_model=SSHWHM)
async def create_sshwhm_product(product: SSHWHMInput, current_user: UserResponse = Depends(get_current_active_seller)):
    if current_user.seller is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not a seller")
    product_dict = product.dict()
    seller_name = current_user.seller.seller_name
    return await create_generic_product(product_dict, "sshwhm", seller_name)

@router.post("/rdp", response_model=RDP)
async def create_rdp_product(product: RDPInput, current_user: UserResponse = Depends(get_current_active_seller)):
    if current_user.seller is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not a seller")
    product_dict = product.dict()
    seller_name = current_user.seller.seller_name
    return await create_generic_product(product_dict, "rdp", seller_name)

@router.post("/smtp", response_model=SMTP)
async def create_smtp_product(product: SMTPInput, current_user: UserResponse = Depends(get_current_active_seller)):
    if current_user.seller is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not a seller")
    product_dict = product.dict()
    seller_name = current_user.seller.seller_name
    return await create_generic_product(product_dict, "smtp", seller_name)

@router.post("/mailers", response_model=Mailers)
async def create_mailers_product(product: MailersInput, current_user: UserResponse = Depends(get_current_active_seller)):
    if current_user.seller is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not a seller")
    product_dict = product.dict()
    seller_name = current_user.seller.seller_name
    return await create_generic_product(product_dict, "mailers", seller_name)

@router.post("/leads", response_model=Leads)
async def create_leads_product(product: LeadsInput, current_user: UserResponse = Depends(get_current_active_seller)):
    if current_user.seller is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not a seller")
    product_dict = product.dict()
    seller_name = current_user.seller.seller_name
    return await create_generic_product(product_dict, "leads", seller_name)

@router.post("/business", response_model=Business)
async def create_business_product(product: BusinessInput, current_user: UserResponse = Depends(get_current_active_seller)):
    if current_user.seller is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not a seller")
    product_dict = product.dict()
    seller_name = current_user.seller.seller_name
    return await create_generic_product(product_dict, "business", seller_name)

@router.post("/accounts", response_model=Accounts)
async def create_accounts_product(product: AccountsInput, current_user: UserResponse = Depends(get_current_active_seller)):
    if current_user.seller is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User is not a seller")
    product_dict = product.dict()
    seller_name = current_user.seller.seller_name
    return await create_generic_product(product_dict, "accounts", seller_name)

# Include the rest of the CRUD operations for other endpoints as required.
