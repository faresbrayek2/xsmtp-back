from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorClient

from app.schemas.ticket import TicketCreate, TicketUpdate, TicketResponse
from app.routes.auth import get_current_user, get_current_active_admin, get_current_active_support
from app.models.user import User
import os
from typing import List
from datetime import datetime

router = APIRouter()

client = AsyncIOMotorClient(os.getenv("MONGODB_URL"))
db = client.xsmtp

# Helper function to get the next ID for tickets
async def get_next_id():
    last_ticket = await db.tickets.find_one(sort=[("id", -1)])
    return (last_ticket["id"] + 1) if last_ticket else 1

@router.post("/tickets/add", response_model=TicketResponse)
async def create_ticket(ticket: TicketCreate, current_user: User = Depends(get_current_user)):
    ticket_dict = ticket.dict()
    ticket_dict["user_id"] = current_user.id
    ticket_dict["id"] = await get_next_id()
    ticket_dict["status"] = "open"
    ticket_dict["messages"] = [{
        "sender_id": current_user.id,
        "content": ticket_dict.pop("initial_message"),
        "timestamp": datetime.utcnow().isoformat()
    }]

    await db.tickets.insert_one(ticket_dict)
    return ticket_dict

@router.get("/tickets", response_model=List[TicketResponse])
async def get_user_tickets(current_user: User = Depends(get_current_user)):
    tickets = await db.tickets.find({"user_id": current_user.id}).to_list(length=100)
    return tickets

@router.get("/tickets/all", response_model=List[TicketResponse])
async def get_all_tickets(current_user: User = Depends(get_current_active_admin)):
    tickets = await db.tickets.find().to_list(length=100)
    return tickets

@router.put("/tickets/{id}", response_model=TicketResponse)
async def update_ticket(id: int, ticket: TicketUpdate, current_user: User = Depends(get_current_user)):
    ticket_dict = ticket.dict(exclude_unset=True)

    existing_ticket = await db.tickets.find_one({"id": id})
    if not existing_ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    if existing_ticket["user_id"] != current_user.id and current_user.role not in ["admin", "support"]:
        raise HTTPException(status_code=403, detail="Not authorized to update this ticket")

    if "messages" in ticket_dict:
        messages = [{
            "sender_id": current_user.id,
            "content": message,
            "timestamp": datetime.utcnow().isoformat()
        } for message in ticket_dict["messages"]]
        existing_ticket["messages"].extend(messages)
        ticket_dict["messages"] = existing_ticket["messages"]

    if current_user.role in ["admin", "support"] and "status" in ticket_dict:
        existing_ticket["status"] = ticket_dict["status"]

    await db.tickets.update_one({"id": id}, {"$set": existing_ticket})
    updated_ticket = await db.tickets.find_one({"id": id})
    return updated_ticket
