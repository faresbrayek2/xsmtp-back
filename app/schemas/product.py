from pydantic import BaseModel, Field
from typing import Dict, Optional
from datetime import datetime
from enum import Enum

# Seller input schemas
class SourceEnum(str, Enum):
    created = "CREATED"
    hacked = "HACKED"

class ShellsInput(BaseModel):
    url: str
    price: float
    source: SourceEnum

class CPanelInput(BaseModel):
    url: str
    username: str
    password: str
    price: float
    source: SourceEnum

class SSHWHMInput(BaseModel):
    url: str
    username: str
    password: str
    price: float
    source: SourceEnum

class RDPInput(BaseModel):
    ip: str
    username: str
    password: str
    source: SourceEnum
    ram: str
    cpu: str
    windows: str
    access: str
    price: float

class SMTPInput(BaseModel):
    ip: str
    port: int
    price: float
    source: SourceEnum

class MailersInput(BaseModel):
    url: str
    price: float
    source: SourceEnum

class LeadsInput(BaseModel):
    url: str
    location: str
    description: str
    niche: str
    website: str
    provider: str
    password: str
    emails_number: int
    proof: str
    price: float

class BusinessInput(BaseModel):
    email: str
    password: str
    price: float
    source: SourceEnum

class AccountsInput(BaseModel):
    email: str
    password: str
    notes: str
    website_domain: str
    location: str
    details: str
    price: float
    source: SourceEnum
    proof: str

# Full product schemas
class Shells(ShellsInput):
    id: Optional[int] = None
    host_info: Optional[str] = None
    location: Optional[str] = None
    ssl: Optional[bool] = None
    tld: Optional[str] = None
    seo_rank_da: Optional[int] = None
    seo_info: Optional[Dict[str, str]] = None
    hosting: Optional[str] = None
    seller: Optional[str] = None
    date_created: datetime = Field(default_factory=datetime.utcnow)

class CPanel(CPanelInput):
    id: Optional[int] = None
    location: Optional[str] = None
    ssl: Optional[bool] = None
    tld: Optional[str] = None
    seo_rank_da: Optional[int] = None
    seo_info: Optional[Dict[str, str]] = None
    hosting: Optional[str] = None
    seller: Optional[str] = None
    date_created: datetime = Field(default_factory=datetime.utcnow)

class SSHWHM(SSHWHMInput):
    id: Optional[int] = None
    host_info: Optional[str] = None
    location: Optional[str] = None
    ram: Optional[str] = None
    hosting: Optional[str] = None
    has_whm: Optional[bool] = None
    seller: Optional[str] = None
    date_created: datetime = Field(default_factory=datetime.utcnow)

class RDP(RDPInput):
    id: Optional[int] = None
    location: Optional[str] = None
    hosting: Optional[str] = None
    ip_blacklist: Optional[bool] = None
    seller: Optional[str] = None
    date_created: datetime = Field(default_factory=datetime.utcnow)

class SMTP(SMTPInput):
    id: Optional[int] = None
    location: Optional[str] = None
    hosting: Optional[str] = None
    seller: Optional[str] = None
    webmail: Optional[str] = None
    date_created: datetime = Field(default_factory=datetime.utcnow)

class Mailers(MailersInput):
    id: Optional[int] = None
    location: Optional[str] = None
    ssl: Optional[bool] = None
    hosting: Optional[str] = None
    seller: Optional[str] = None
    date_created: datetime = Field(default_factory=datetime.utcnow)

class Leads(LeadsInput):
    id: Optional[int] = None
    location: Optional[str] = None
    niche: Optional[str] = None
    proof: Optional[str] = None
    seo_rank_da: Optional[int] = None
    seo_info: Optional[Dict[str, str]] = None
    seller: Optional[str] = None
    date_created: datetime = Field(default_factory=datetime.utcnow)

class Business(BusinessInput):
    id: Optional[int] = None
    location: Optional[str] = None
    website: Optional[str] = None
    hosting: Optional[str] = None
    type: Optional[str] = None
    niche: Optional[str] = None
    seller: Optional[str] = None
    date_created: datetime = Field(default_factory=datetime.utcnow)

class Accounts(AccountsInput):
    id: Optional[int] = None
    notes: Optional[str] = None
    seller: Optional[str] = None
    date_created: datetime = Field(default_factory=datetime.utcnow)
